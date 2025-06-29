from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
import models
import schemas
import security
import database

# Criando as tavelas no banco de dados
database.create_db_and_tables()

app = FastAPI()

#============ Endpoint para cadastro de usuário ============
@app.post("/users/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email já cadastrado")
    return crud.create_user(db=db, user=user)


#============ Endpoint para login de usuário ============
@app.post("/token", response_model=schemas.Token)
def login_acess_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    #busca o usuário pelo email
    #mas como o formulario é OAuth2PasswordRequestForm, o email é o username
    #então é preciso usar form_data.username para pegar o email
    user = crud.get_user_by_email(db, email=form_data.username) 

    #verifica se o usuário existe e se a senha está correta
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    #gera o token de acesso
    access_token = security.create_acess_token(data={"sub": user.email})


    return {"access_token": access_token, "token_type": "bearer"}
