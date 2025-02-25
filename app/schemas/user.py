from pydantic import BaseModel, EmailStr, constr
from typing import Union, Optional
from enum import Enum


class RoleType(str, Enum):
    ADMIN = "ADMIN"
    FUNCIONARIO = "FUNCIONARIO"
    GERENTE = "GERENTE"
    ADMIN_SEGURANCA = "ADMIN_SEGURANCA"

class RoleOUt(BaseModel):
    role_type: RoleType

    class Config:
        orm_mode = True
    

# Cria um Modelo de usuario com role padrão com Funcionario
class UserIn(BaseModel):    
    username: constr(min_length=1, strip_whitespace=True)  # Não pode ser vazio str
    email: EmailStr
    password: constr(min_length=4, strip_whitespace=True)  # Não pode ser vazio str
    role: Optional[RoleType] = RoleType.FUNCIONARIO 

# Cria um modelo para representar um usuario existente no Banco de Dados
class UserOut(UserIn):
    id: Optional [int]
    is_active: Optional [bool] = True # Por padrão o usuario é ativo
    is_admin: Optional [bool] = False # Por padrão o usuario não é admin
    role: Optional [RoleType] = RoleType.FUNCIONARIO # Por padrão o usuario é um Funcionario
    password: Optional [str] = None # fara com que a senha não seja retornada

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



