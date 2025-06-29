from sqlalchemy import Column, Integer, String
from database import Base  # Importa a Base declarativa

class User(Base):
    """Modelo da Tabela de Usuário."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"