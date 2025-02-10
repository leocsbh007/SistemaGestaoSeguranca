from pydantic import BaseModel
from typing import Union, Optional
from enum import Enum


class RoleType(str, Enum):
    ADMIN = "admin"
    FUNCIONARIO = "funcionario"
    GERENTE = "gerente"
    ADMIN_SEGURANCA = "admin_seguranca"

# Cria um Modelo de usuario
class UserBase(BaseModel):
    username: str
    email: str

# Cria um Modelo de usuario com role padrão com Funcionario
class UserCreate(UserBase):    
    password: str
    role: Optional[RoleType ]= RoleType.FUNCIONARIO 

# Cria um modelo para representar um usuario existente no Banco de Dados
class User(UserBase):
    id: Optional [int]
    is_active: Optional [bool]
    is_admin: Optional [bool]

    class Config:
        #from_attributes = True
        orm_mode = True

#
class Token(BaseModel):
    access_token: str
    token_type: str

#
class TokenData(BaseModel):
    username: Union[str, None] = None



