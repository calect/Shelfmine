import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import time

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Pega a URL do banco de dados a partir das variáveis de ambiente
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Cria o motor (engine) do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma classe SessionLocal configurada.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Retorna uma classe. Nossos modelos de tabela irão herdar desta classe.
Base = declarative_base()

def get_db():
    """Função para obter uma sessão do banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_db_and_tables():
    """
    Cria todas as tabelas no banco de dados que são declaradas em Base.
    Esta função é chamada na inicialização da aplicação.
    """
    print("Tentando conectar ao banco de dados para criar tabelas...")
    
    retries = 10
    while retries > 0:
        try:
            # Tenta estabelecer uma conexão real
            connection = engine.connect()
            connection.close()
            print("Conexão com o banco de dados bem-sucedida.")
            
            # Cria as tabelas
            Base.metadata.create_all(bind=engine)
            print("Tabelas criadas com sucesso (se não existirem)!")
            break
        except Exception as e:
            print(f"Erro ao conectar ou criar tabelas: {e}")
            retries -= 1
            print(f"Nova tentativa em 5 segundos... ({retries} tentativas restantes)")
            time.sleep(5)