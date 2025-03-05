from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
from app.schemas.resource import ResourceOut
from app.schemas.user import UserOut
from enum import Enum

class LoanStatus(str, Enum):
    ATIVO = "ATIVO"
    FINALIZADO = "FINALIZADO"
    ATRASADO = "ATRASADO"

class LoanIn(BaseModel):
    user_id: int
    resource_id: int
    start_date: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    loan_duration_hours: int = Field(24,description="Duração do empréstimo em horas (padrão: 24h)")
    status: LoanStatus = LoanStatus.ATIVO

    class Config:
        orm_mode = True

class LoanOut(LoanIn):
    id: int
    calculated_end_date: datetime
    # user: UserOut  # Dados do usuário que fez o empresitmo
    # resource: ResourceOut    # Dados do recurso emprestado

    class Config:
        orm_mode = True
