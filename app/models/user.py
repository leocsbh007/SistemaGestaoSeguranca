from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class RoleType(enum.Enum):
    ADMIN = "ADMIN"
    FUNCIONARIO = "FUNCIONARIO"
    GERENTE = "GERENTE"
    ADMIN_SEGURANCA = "ADMIN_SEGURANCA"
 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True) # Padrão usuario Ativo
    is_admin = Column(Boolean, default=False) # Padrão não ser Admin
    
    role = relationship("Role", back_populates="user", uselist=False, cascade="all, delete") # Relação com a tabela Role
    resources = relationship("Resource", back_populates="user", cascade="all, delete") # Relação com a tabela Resource

    # Relacionamento com a tabela de empréstimos (Loans)
    loans = relationship("Loan", back_populates="user", cascade="all, delete") # Relação com a tabela Loan


class Role(Base):
    __tablename__ = "roles" # Nome da Tabela no Banco

    id = Column(Integer, primary_key=True, index=True)
    role_type = Column(Enum(RoleType), default=RoleType.FUNCIONARIO)    # Pega o enum da class RoleType

    # Chave estrangeira que se refere à tabela de users
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE")) # Chave estrangeira para a tabela User

    user = relationship("User", back_populates="role") # Relação com a tabela User


