from pydantic import BaseModel
from typing import Union
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
    role: RoleType = RoleType.FUNCIONARIO 

# Cria um modelo para representar um usuario existente no Banco de Dados
class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True

#
class Token(BaseModel):
    access_token: str
    token_type: str

#
class TokenData(BaseModel):
    username: Union[str, None] = None



