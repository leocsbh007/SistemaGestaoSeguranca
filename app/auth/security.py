from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta
from app.services.auth import verify_password
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Cria um contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para hash de senha
def hash_password(password: str) -> str:    
    return pwd_context.hash(password)

# Função para verificar a Senha
def verify_password(entered_password, hashed_password) -> bool:    
    return pwd_context.verify(entered_password, hashed_password)

# Função para criar um token jwt
def create_token(data : dict):
    to_encode = data.copy()    
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)    
    to_encode["exp"] = expires.timestamp() # Converte datetime para Timestamp
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)