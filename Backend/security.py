# Transofrmando as senha de string para hash para armazenar no banco de dados
from passlib.context import CryptContext

# Usando o algoritmo "bcrypt" para criptograr pois ele dificulta ataques  
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
