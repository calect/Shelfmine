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