from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models import user as user_db  # Para o modelo do banco
from app.schemas.user import UserIn, UserOut
from app.services.user import register_user
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

# Cria um roteador para a rota de usuarios
router = APIRouter()

# Criando um novo usuario
@router.post("/users", response_model=UserOut,dependencies=[Depends(require_admin)] status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserIn, db: Session = Depends(get_db)):
    '''Rota para criar um novo usuario'''
    try:
        return register_user(db, user_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar o Usuario, usuário já existe"
        )    
    
    
# Deletando um usuario
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # print(f'User ID: {user_id}')

    try:
        # Busca o usuario no banco de dados
        db_user = db.query(user_db.DBUser).filter(user_db.DBUser.id == user_id).first()
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


    