from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models import user as user_db
from app.schemas.user import UserIn
from app.auth import security
from app.repositories import user as user_repositories
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

# Roteador para as rotas de autenticação
router = APIRouter()

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Criando a Rota de Login
@router.post("/login")
def login(user_in: UserIn, db: Session = Depends(get_db)):
    # Busca usuario no Banco de Dados    
    db_user = user_repositories.get_user_by_email(db, user_in.email)   
    
    # Verifica se o usuário existe antes de acessar seus atributos
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Verifica se o usuário está ativo
    if user_repositories.get_user_is_active(db, db_user.username) == False:        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    #Verifica se o usuario existe
    if user_repositories.get_user_by_username(db, user_in.username) is None:        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario não encontrado"
        )
    
    # Verifica se a senha está correta
    if not security.verify_password(user_in.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha Incorreta",
            #headers={"WWW-Authenticate" : "Beares"}
            headers={"WWW-Authenticate": "Bearer"}
        )
    # Cria o Token Jwt    
    token = security.create_access_token({"sub" : db_user.email})
    
    # Busca a Role desse Usuario e atualiza pelo Valor de entrada
    db_role = db.query(user_db.DBRole).filter(user_db.DBRole.user_id == db_user.id).first()
    if db_role is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Role do usuário não encontrada"
        )

    response_data = {
        "access_token": token,
        "token_type": "bearer",
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "is_active": db_user.is_active,
        "is_admin": db_user.is_admin,
        "role": db_role.role_type
    }    

    return response_data



# Rota para obter os dados de usuario autenticado
@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    # print(f"Token: {token}")
    payload = security.decode_access_token(token)
    # print(f"Payload: {payload}")
    return {"user": payload}
