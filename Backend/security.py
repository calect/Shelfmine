# Transofrmando as senha de string para hash para armazenar no banco de dados
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
import os

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
# ==========================================================
# LINHAS DE DEBUG: Vamos imprimir o valor para ver o que o Python está enxergando.
print("--- INICIANDO VERIFICAÇÃO DE DEBUG ---")
print(f"!!! A CHAVE SECRETA CARREGADA É: {SECRET_KEY} !!!")
print(f"!!! O TIPO DA CHAVE SECRETA É: {type(SECRET_KEY)} !!!")
print("--- FIM DA VERIFICAÇÃO DE DEBUG ---")
# ==========================================================

ALGORITHM = "HS256" 
ACESS_TOKEN_EXPIRE_MINUTES = 30  # Login expira em 30 min

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

