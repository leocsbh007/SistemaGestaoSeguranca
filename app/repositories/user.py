from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.user import DBUser, DBRole
from app.schemas.user import UserIn
from app.auth import security
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)


def get_user_by_email(db: Session, email: str) -> DBUser | None:
    '''Retorna um usuario pelo email'''
    return db.query(DBUser).filter(DBUser.email == email).first()

def get_user_by_username(db: Session, username: str) -> DBUser | None:
    '''Retorna um usuario pelo nome'''
    return db.query(DBUser).filter(DBUser.username == username).first()


def get_user_is_active(db: Session, user_id: int) -> bool:
    '''Verifica se o usuario está ativo'''
    db_user = get_user_by_username(db, db_user.username)
    if db_user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário Não Está Ativo",
            headers={"WWW-Authenticate" : "Beares"}
        )
    return True

def create_user(db: Session, user_in: UserIn) -> DBUser:

    try:        
        hashed_password_in = security.hash_password(user_in.password)

        # Cria um Objeto Usuario para adicionar no Banco
        db_user = DBUser(
            username=user_in.username,
            hashed_password = hashed_password_in,
            email=user_in.email
        )

        # Cria um Objeto role para adicionar no Banco
        db_role = DBRole(
            role_type=user_in.role,
            user=db_user
        )
        # print(f'Role: {new_role.role_type}')
       
        # Verifica se o usuario é Admin 
        if db_role.role_type == 'ADMIN':            
            db_user.is_admin = True
        
        # Adiciona o novo Role no Banco
        db.add(db_role)

        # Adiciona o novo Usuario no Banco
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        #LOG do cadastros
        logger.info(f"Usuário {db_user.username} criado com Sucesso com a role {user_in.role}.")        

        # Retorna os dados como Pydantic (convertendo o objeto SQLAlchemy)
        # Conversão usando from_orm
        return db_user        

    except Exception as e:
        logger.error(f"Erro ao criar o usuário {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar o Usuario"
        )
