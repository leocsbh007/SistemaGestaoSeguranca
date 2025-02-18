from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.models import user as user_db  # Para o modelo do banco
from app.schemas.user import UserIn, UserOut
from app.services.user import register_user
from app.auth.middleware import require_admin
from app.repositories import user as user_repositories
from app.auth import security
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
@router.put("/users/{user_id_put}", response_model=UserOut, dependencies=[Depends(require_admin)])
def update_user(user_id_put: int, user_in: UserIn, db: Session = Depends(get_db)):
    db_user = user_repositories.get_user_by_id(db, user_id_put)
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
    
    # Faz o hash da Senha digitada pelo usuario
    hashed_password_in = security.hash_password(user_in.password)
    # Atualiza os campos para inserir no Banco
    db_user.username = user_in.username
    db_user.hashed_password = hashed_password_in
    db_user.email = user_in.email

    
    # Busca a Role desse Usuario e atualiza pelo Valor de entrada
    db_role = db.query(user_db.DBRole).filter(user_db.DBRole.user_id == user_id_put).first()
    if db_role is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Role do usuário não encontrada"
        )
    
    # Verifica se a Role do Usuario precisa ser alterada
    if db_role.role_type != user_in.role:
        db_role.role_type=user_in.role
        

    # Verifica se o usuario é Admin 
    if user_in.role == 'ADMIN':            
        db_user.is_admin = True
    
    # Adiciona o novo Role no Banco
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Erro ao atualizar o usuário no banco de dados"
        )

    return db_user
    
    
    

    


    