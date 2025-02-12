from pydantic import BaseModel
from typing import Optional
from enum import Enum

class ResourceType(str, Enum):
    EQUIPAMENTO = "EQUIPAMENTO"
    VEICULO = "VEICULO"
    DISPOPSITIVO_SEGURANCA = "DISPOSITIVO_SEGURANCA"


class StatusType(str, Enum):
    DISPONIVEL = "DISPONIVEL"
    EM_USO = "EM_USO"
    MANUTENCAO = "MANUTENCAO"

class ResourceBase(BaseModel):
    name: str
    description: Optional[str] = None
    type : Optional [ResourceType] = None   # Tipo de recurso, deve ser adiciona quando o recurso for criado, pois ainda não sabemos o tipo até o usuário informar
    status: StatusType = StatusType.DISPONIVEL

    class Config:
        orm_mode = True     # Permite que o Pydantic possa entender o retorno do ORM

class ResourceResponse(ResourceBase):
    id: int     # O ID é obrigatório para a resposta
    assigned_to : Optional[int] = None # ID do usuário que está com o recursos, por padrão é None, pois o recurso está disponível

    class Config:
        orm_mode = True