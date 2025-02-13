from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models import user as user_db  # Para o modelo do banco
from app.schemas import user as schema_user # Para o modelo schema do pydantic
from app.services import auth
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

# Cria um roteador para a rota de usuarios
router = APIRouter()

# Banco Mocado
mocado_db_users = []

# Criando um novo usuario
@router.post("/register", response_model=schema_user.User, status_code=status.HTTP_201_CREATED)
def register(user_data: schema_user.UserCreate, db: Session = Depends(get_db)):
    
    
    
# Deletando um usuario
@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # print(f'User ID: {user_id}')

    try:
        # Busca o usuario no banco de dados
        db_user = db.query(user_db.User).filter(user_db.User.id == user_id).first()
        # print(f'Id User: {db_user.id}')
        # print(f"Usuário encontrado: {db_user.id}, Role: {db_user.role}")  # <- DEBUG
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario não encontrado"
            )
        

        # Deleta o usuario
        db.delete(db_user)
        db.commit()
        return {"detail": "Usuario deletado com sucesso"}
    
    except Exception as e:
        logger.error(f"Erro ao deletar o usuario {e}")        
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar o usuario"
        )


    