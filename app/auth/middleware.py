
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.auth.security import decode_access_token
from app.repositories import user as user_repo
from app.models.user import RoleType
from app.models.base import get_db
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> user_repo.DBUser:
    payload = decode_access_token(token)        
    print(f"Payload: {payload}")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Inválido, ou Expirado"
        )
    user_email = payload.get("sub")
    db_user = user_repo.get_user_by_email(db, user_email)
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuário Não Encontrado"
        )
    
    return db_user


def require_admin(current_user = Depends(get_current_user)):
    '''Função para verificar se o usuário é um admin'''
    if current_user.role.role_type != RoleType.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso Negado. Apenas ADMINs podem acessar esse recurso"
        )
    return current_user