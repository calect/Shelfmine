from pydantic import BaseModel
from typing import List # Para listas

# --- Fluxo de Item --- 

# Schema base para um Item
class ItemBase(BaseModel):
    title: str
    description: str | None = None

# Schema para criar um Item (recebido pela API)
class ItemCreate(ItemBase):
    pass

# Schema para ler um Item (retornado pela API)
class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


# --- Fluxo de User---

# Criando um user
class UserCreate(BaseModel):   
    email: str
    password: str

# Lendo um user
class User(BaseModel):
    id: int
    email: str
    items: List[Item] = [] # Mostra os itens que o usuário possui

    class Config:
        from_attributes = True # Pydantic irá ler os atributos do modelo SQLAlchemy

# ---  Autenticação (Token) ---

# Login Sucedido - formato do JSON  retornado
class Token(BaseModel):
    access_token: str
    token_type: str

# Estrutura do token JWT
class TokenData(BaseModel):
    email: str | None = None