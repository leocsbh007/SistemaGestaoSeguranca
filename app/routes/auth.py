from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from app.models.base import get_db
from app.models import user as user_db  # Para o modelo do banco
from app.services.auth import verify_password
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

# Roteador para as rotas de autenticação
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Função para criar um token jwt
def create_token(data:dict, expires_delta):
    to_encode = data.copy()    
    expires = datetime.utcnow() + expires_delta
    #to_encode.update({"expira" : expires})
    to_encode["exp"] = expires.timestamp() # Converte datetime para Timestamp
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Criando a Rota de Login
# @router.post("/login", response_model=schema_user.User)
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # print("Form Data: ", form_data)

    # Busca usuario no Banco de Dados
    db_user = db.query(user_db.DBUser).filter(user_db.DBUser.username == form_data.username).first()
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário Não encontrado",
            headers={"WWW-Authenticate" : "Beares"}
        )
    
    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Senha Incorretos",
            headers={"WWW-Authenticate" : "Beares"}
        )
    # Cria o Token Jwt
    # print(f"Gerando o token para Usuario {db_user.username}")    
    token = create_token({"sub" : db_user.username})

    # print(f"Token Gerado: {token}")  # <--- Adicionando log para depuração

    response_data = {
        "access_token": token,
        "token_type": "bearer",
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "is_active": db_user.is_active,
        "is_admin": db_user.is_admin
    }

    # print(f"Resposta Final: {response_data}")  # <--- Adicionando log para depuração

    return response_data


# Decodificando o Token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWKError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token Invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
# Rota para obter os dados de usuario autenticado
@router.get("/me")
def read_users_me(token: str = Depends(oauth2_scheme)):
    # print(f"Token: {token}")
    payload = decode_token(token)
    # print(f"Payload: {payload}")
    return {"user": payload}