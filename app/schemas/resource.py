from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

# Definição dos tipos de recursos e status
class ResourceType(str, Enum):
    EQUIPMENTO = 'EQUIPAMENTO'
    VEICULO = 'VEICULO'
    DISPOSITIVO_SEGURANCA = 'DISPOSITIVO_SEGURANCA'

class StatusType(str, Enum):
    DISPONIVEL = 'DISPONIVEL'
    EM_USO = 'EM USO'
    MANUTENCAO = 'MANUTENCAO'

# Esquema para criação de um novo recurso
class ResourceCreate(BaseModel):
    name: str
    type: ResourceType
    description: str
    status: StatusType = StatusType.DISPONIVEL

    class Config:
        orm_mode = True

# Esquema para atualização de um recurso
class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[ResourceType] = None
    description: Optional[str] = None
    status: Optional[StatusType] = None

    class Config:
        orm_mode = True

# Esquema de saída (resposta da API)
class ResourceOut(BaseModel):
    id: int
    name: str
    type: ResourceType
    description: str
    status: StatusType
    assigned_to: Optional[int]
    
    class Config:
        orm_mode = True
