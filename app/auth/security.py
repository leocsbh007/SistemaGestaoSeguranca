from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext


# Cria um contexto de criptografia
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Função para hash de senha
def hash_password(password: str) -> str:    
    return pwd_context.hash(password)

# Função para verificar a Senha
def verify_password(entered_password, hashed_password) -> bool:    
    return pwd_context.verify(entered_password, hashed_password)

# Função para criar um token jwt
def create_access_token(data : dict) -> str:
    '''Gera um Token de Acesso com base em um dicionário de dados com duração de ACCESS_TOKEN_EXPIRE_MINUTES minutos'''
    to_encode = data.copy()    
    expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)    
    to_encode["exp"] = expires.timestamp() # Converte datetime para Timestamp
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Decodificando o Token
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token Invalido",
        headers={"WWW-Authenticate": "Bearer"},
        )
        return None
    
    