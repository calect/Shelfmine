from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import httpx
import os


import crud
import models
import schemas
import security
import database

# Criando as tabelas no banco de dados
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

#============ Endpoint para Criar um Item para o Usuário Logado ============
@app.post("/users/me/items/", response_model=schemas.Item, tags=["Items"])
def create_item_for_current_user(
    item: schemas.ItemCreate,
    current_user: schemas.User = Depends(security.get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Cria um item (livro) associado ao usuário atualmente autenticado.
    O FastAPI irá garantir que apenas usuários com um token válido possam acessar este endpoint.
    """
    return crud.create_user_item(db=db, item=item, user_id=current_user.id)

#============ Endpoint para Deletar um Item ============
@app.delete("/items/{item_id}", response_model=schemas.Item, tags=["Items"])
def delete_user_item(
    item_id: int,
    current_user: schemas.User = Depends(security.get_current_user),
    db: Session = Depends(database.get_db)
):
    """
    Deleta um item. Apenas o dono do item pode deletá-lo.
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    # Verifica se o usuário logado é o dono do item
    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Sem autorização para deletar esse item")

    crud.delete_item(db, item_id=item_id)
    return db_item

#============ Endpoint para Busca de Livros pela API GOOGLR BOOKS=============  
@app.get("/books/search/",tags=["Busca externa"])

#usando um query q de busca para procurar os livros.
async def search_books(q:str):
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Chave da API do Google Books não configurada."
        )
    #Monsta a url e busca até 10 resultados
    url = f"https://www.googleapis.com/books/v1/volumes?q={q}&key={api_key}"
    
    async with httpx.AsyncClient() as client:
        try:
            google_response = await client.get(url)
            google_response.raise_for_status()  # Lança um erro se a resposta não for 2xx
            return google_response.json()

        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503, 
                detail="Erro de comunicação com API do google"
                )