from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base
import enum
from datetime import datetime, timezone

class LonasStatus(enum.Enum):
    ATIVO = 'ATIVO'
    FINALIZADO = 'FINALIZADO'
    ATRASADO = 'ATRASADO'

class DBLoan(Base):
    __tablename__ = 'loans'

    id = Column(Integer, primary_key=True, index=True) # Identificador do empréstimo
    start_date = Column(DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)) # Data de início do empréstimo, obrigatório
    end_date = Column(DateTime, nullable=False) # Data de fim do empréstimo, obrigatório
    status = Column(Enum(LonasStatus), nullable=False, default=LonasStatus.ATIVO) # Status do empréstimo, obrigatório. Deve ser um dos valores definidos em LonasStatus


    # Definição do relacionamento com a tabela de usuários
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # Chave estrangeira para a tabela User    
    user = relationship("DBUser", back_populates="loan")  # Relação com a tabela User

    # Definição do relacionamento com a tabela de recursos    
    resource_id = Column(Integer, ForeignKey("resources.id", ondelete="CASCADE"), nullable=False)  # Chave estrangeira para a tabela Resource
    resource = relationship("DBResource", back_populates="loan")  # Relação com a tabela Resource

