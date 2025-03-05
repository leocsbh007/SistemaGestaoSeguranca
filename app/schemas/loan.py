from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
from .resource import ResourceResponse
from .user import UserBase
from enum import Enum

class LoanStatus(str, Enum):
    ATIVO = "ATIVO"
    FINALIZADO = "FINALIZADO"
    ATRASADO = "ATRASADO"

class LoanBase(BaseModel):
    star_date: datetime = Field(default = lambda: datetime.now(timezone.utc)) # Data de início do empréstimo, obrigatório 
    end_date: datetime # Data de fim do empréstimo, obrigatório
    status: LoanStatus = LoanStatus.ATIVO # Status do empréstimo, obrigatório. Deve ser um dos valores definidos em LoanStatus

    class Config:
        orm_mode = True

class LoanCreate(LoanBase):
    user_id: int    # ID do usuário que está pegando o recurso
    resource_id: int    # ID do recurso que está sendo pego

class LoanResponse(LoanBase):
    id: int    # ID do empréstimo
    user: UserBase  # Dados do usuário que fez o empresitmo
    resource: ResourceResponse    # Dados do recurso emprestado

    class Config:
        orm_mode = True
