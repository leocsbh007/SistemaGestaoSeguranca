from pydantic import BaseModel, EmailStr
from typing import Union, Optional
from enum import Enum


class RoleType(str, Enum):
    ADMIN = "ADMIN"
    FUNCIONARIO = "FUNCIONARIO"
    GERENTE = "GERENTE"
    ADMIN_SEGURANCA = "ADMIN_SEGURANCA"
    
# Cria um Modelo de usuario
class UserBase(BaseModel):
    username: str
    email: EmailStr

# Cria um Modelo de usuario com role padrão com Funcionario
class UserCreate(UserBase):    
    password: str
    role: Optional[RoleType] = RoleType.FUNCIONARIO 

# Cria um modelo para representar um usuario existente no Banco de Dados
class User(UserBase):
    id: Optional [int]
    is_active: Optional [bool] = True # Por padrão o usuario é ativo
    is_admin: Optional [bool] = False # Por padrão o usuario não é admin

    class Config:
        #from_attributes = True
        orm_mode = True # Permite que o Pydantic possa entender o retorno do ORM

# Modelo para token JWT
class Token(BaseModel):
    access_token: str
    token_type: str

# Modelo para dados do token
class TokenData(BaseModel):
    username: Union[str, None] = None



