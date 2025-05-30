from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

class RoleType(enum.Enum):
    ADMIN = "ADMIN"
    FUNCIONARIO = "FUNCIONARIO"
    GERENTE = "GERENTE"
    ADMIN_SEGURANCA = "ADMIN_SEGURANCA"
 

class DBUser(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True) # Padrão usuario Ativo
    is_admin = Column(Boolean, default=False) # Padrão não ser Admin
    
    role = relationship("DBRole", back_populates="user", uselist=False, cascade="all, delete")  # Relação com a tabela Role    
    resource = relationship("DBResource", back_populates="user", cascade="all", passive_deletes=True)  # Remove a referência, não apaga o recurso
    loan = relationship("DBLoan", back_populates="user", cascade="all, delete")  # Relação com a tabela Loan

class DBRole(Base):
    __tablename__ = "roles" # Nome da Tabela no Banco

    id = Column(Integer, primary_key=True, index=True)
    role_type = Column(Enum(RoleType), default=RoleType.FUNCIONARIO)    # Pega o enum da class RoleType

    # Chave estrangeira que se refere à tabela de users
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE")) # Chave estrangeira para a tabela User

    user = relationship("DBUser", back_populates="role") # Relação com a tabela User


