from pydantic import BaseModel
from enum import Enum
from typing import Optional

# Definição dos tipos de recursos e status
class ResourceType(str, Enum):
    EQUIPAMENTO = 'EQUIPAMENTO'
    VEICULO = 'VEICULO'    
    DISPOSITIVO_SEGURANCA = 'DISPOSITIVO_SEGURANCA'

class StatusType(str, Enum):
    DISPONIVEL = 'DISPONIVEL'
    EM_USO = 'EM_USO'
    MANUTENCAO = 'MANUTENCAO'

# Esquema para criação de um novo recurso
class ResourceIn(BaseModel):
    asset_number: str
    name: str
    type: ResourceType
    description: str
    status: StatusType = StatusType.DISPONIVEL

    class Config:
        orm_mode = True

# Esquema para atualização de um recurso
class ResourceOut(ResourceIn):
    id: Optional[int]    
    
    class Config:
        orm_mode = True


