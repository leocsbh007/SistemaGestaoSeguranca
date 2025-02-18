from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models import user as user_db  # Para o modelo do banco
from app.schemas.user import UserIn, UserOut
from app.services.user import register_user
from app.auth.middleware import require_admin
from app.repositories import user as user_repositories
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

# Cria um roteador para a rota de usuarios
router = APIRouter()

# Rota para listar todos os usuarios
@router.get("/users/", response_model=list[UserOut], dependencies=[Depends(require_admin)])
def get_users(db: Session = Depends(get_db)):
    '''Rota para listar todos os usuarios'''
    return db.query(user_db.DBUser).all()

# Rota para buscar um usuario pelo ID
@router.get("/users/{user_id}", response_model=UserOut, dependencies=[Depends(require_admin)])
def get_user(user_id: int, db: Session = Depends(get_db)):
    '''Rota para buscar um usuario pelo ID'''
    db_user = db.query(user_db.DBUser).filter(user_db.DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario não encontrado"
        )
    return db_user

# Criando um novo usuario
@router.post("/users/", response_model= UserOut, dependencies=[Depends(require_admin)], status_code=status.HTTP_201_CREATED)
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
@router.delete("/users/{user_id}", dependencies=[Depends(require_admin)])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # print(f'User ID: {user_id}')
    '''Rota para buscar um usuario pelo ID'''
    db_user = db.query(user_db.DBUser).filter(user_db.DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario não encontrado"
        )    

    try:
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


# Altera Usuario
@router.put("/users/{user_id}", response_model=UserOut, dependencies=[Depends(require_admin)])
def update_user(user_id: int, user_in: UserIn, db: Session):
    db_user = user_repositories.get_user_by_id(db, user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Usuario não encontrado'
        )
    
    exist_user = user_repositories.get_user_by_email(db, user_in.email)
    if exist_user is not None and exist_user.id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Já existe um usuario cadastrado com este e-mail'
        )
    
    
    user_repositories.create_user(db, user_in)
    

    


    