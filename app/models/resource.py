from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum

# Definição dos tipos de recursos e status
class ResourceType(enum.Enum):
    EQUIPAMENTO = 'EQUIPAMENTO'
    VEICULO = 'VEICULO'    
    DISPOSITIVO_SEGURANCA = 'DISPOSITIVO_SEGURANCA'

class StatusType(enum.Enum):
    DISPONIVEL = 'DISPONIVEL'
    EM_USO = 'EM_USO'
    MANUTENCAO = 'MANUTENCAO'


# Definição da classe de recursos
class DBResource(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True, index=True) # Identificador do recurso
    asset_number = Column(String, nullable=False) # Número de patrimônio do recurso, obrigatório
    name = Column(String, nullable=False) # Nome do recurso, obrigatório
    type = Column(Enum(ResourceType), nullable=False) # Tipo do recurso, obrigatório. Deve ser um dos valores definidos em ResourceType
    description = Column(String, nullable=False) # Descrição do recurso, obrigatório
    status = Column(Enum(StatusType), nullable=False, default=StatusType.DISPONIVEL) # Status do recurso, obrigatório. Deve ser um dos valores definidos em StatusType


    # Definição do relacionamento com a tabela de users    
    assigned_to = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # Chave estrangeira para a tabela User, pode ser nula
    user = relationship("DBUser", back_populates="resource")  # Relação com a tabela User


    # Relacionamento com a tabela de empréstimos (Loans)    
    loan = relationship("DBLoan", back_populates="resource", cascade="all, delete")  # Relação com a tabela Loan


    