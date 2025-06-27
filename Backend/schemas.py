from pydantic import BaseModel

# --- Fluxo de User---

# Criando um user
class UserCreate(BaseModel):   
    email: str
    password: str

# Lendo um user
class User(BaseModel):
    id: int
    email: str

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