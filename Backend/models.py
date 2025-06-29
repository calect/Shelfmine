from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base  # Importa a Base declarativa
from sqlalchemy.orm import relationship

class User(Base):
    """Modelo da Tabela de Usuário."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relacionamento com a tabela de Itens
    items = relationship("Item", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"
    
# Tabela para os Itens (Livros)
class Item(Base):
    """Modelo da Tabela de Item (Livro)."""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    
    # Chave Estrangeira (ForeignKey)
    # Esta coluna armazena o ID do usuário que é dono deste item.
    # A sintaxe "users.id" se refere à coluna 'id' da tabela 'users'.
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Relacionamento reverso com a tabela User
    # Cria uma propriedade .owner em cada objeto Item,
    # que aponta de volta para o objeto User correspondente.
    owner = relationship("User", back_populates="items")
