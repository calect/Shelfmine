from sqlalchemy.orm import Session
import models
import schemas
import security

# Buscar um user pelo email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Criar um novo user no banco
def create_user(db: Session, user: schemas.UserCreate):
    #gerar o hash da senha
    hashed_password = security.get_password_hash(user.password)
    # Cria o obj SQLAlchemy com o email e a senha hasheada
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    # Adiciona ao banco
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Funções CRUD para Item --- 

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """Retorna uma lista de todos os itens. """
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    """Cria um novo item e o associa a um usuário pelo seu ID."""
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: int):
    """Busca um item específico pelo seu ID."""
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def delete_item(db: Session, item_id: int):
    """Deleta um item do banco de dados pelo seu ID."""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item