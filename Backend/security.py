# Transofrmando as senha de string para hash para armazenar no banco de dados
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import os

import schemas
import database

#===================== Hash da senha =========================
# Usando o algoritmo "bcrypt" para criptograr pois ele dificulta ataques 
# pois é um algoritmo de hash lento, o que torna mais difícil para os atacantes
# quebrar as senhas por força bruta. 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para verificar se a senha informada é igual a senha armazenada
def verify_password(password, hashed_password):
    # Usada no  login
    # ela compara a senha digitada pelo user com o hash armazenado no banco de dados
    return pwd_context.verify(password, hashed_password)

# Função para criar o hash da senha
def get_password_hash(password: str) -> str:
    #Usada na hora do cadastro
    #ela transforma a senha em um hash e salva no banco de dados
    return pwd_context.hash(password)

#==================== Autenticação com JWT =========================

# Chave secreta para assinar os tokens JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256" 
ACESS_TOKEN_EXPIRE_MINUTES = 30  # Login expira em 30 min

# Instância do esquema de segurança OAuth2
# aponta para o endpoint /token criado
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Função para gerar o token
def create_acess_token(data: dict):
    # Cria um token JWT com os dados fornecidos
    to_encode = data.copy() # data = email do user
    # Define o tempo de expiração do token
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # Gera o token usando a chave secreta e o hash 256
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Função para obter o usuário logado atualmente
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    """
    Decodifica o token, extrai o email (id) do usuário, busca no banco
    e retorna o objeto User. Usado como uma dependência em endpoints protegidos.
    """
    import crud
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica o token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # Valida o schema dos dados do token
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    # Busca o usuário no banco de dados
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    
    return user