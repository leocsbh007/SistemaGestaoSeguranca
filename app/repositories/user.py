from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.user import DBUser, DBRole, RoleType
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
    response = db.query(DBUser).filter(DBUser.username == username).first()    
    #return db.query(DBUser).filter(DBUser.username == username).first()
    return response

def get_user_by_id(db: Session, user_id: int) -> DBUser | None:
    '''Retorna um usuario pelo id'''
    response = db.query(DBUser).filter(DBUser.id == user_id).first()        
    return response



def get_user_is_active(db: Session, user_name: str) -> bool:
    '''Verifica se o usuario está ativo'''
    db_user = get_user_by_username(db, user_name)    
    if db_user.is_active == False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário Não Está Ativo",
            headers={"WWW-Authenticate" : "Beares"}
        )
    return True

def create_user(db: Session, user_in: UserIn) -> DBUser:

    try:        
         # Validação do role
        try:
            new_role = RoleType(user_in.role)  # Converte a string para enum
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role inválida: {user_in.role}. Deve ser um dos seguintes: {[r.value for r in RoleType]}"
            )
        
        hashed_password_in = security.hash_password(user_in.password)

        # Cria um Objeto Usuario para adicionar no Banco
        db_user = DBUser(
            username=user_in.username,
            hashed_password = hashed_password_in,
            email=user_in.email
        )

        # Cria um Objeto role para adicionar no Banco
        db_role = DBRole(
            role_type=new_role,
            user=db_user
        )

        # Atualiza a role se necessário
        if db_role.role_type != new_role:
            db_role.role_type = new_role   

        # Verifica se o usuário deve ser admin
        db_user.is_admin = new_role == RoleType.ADMIN
        
        # Adiciona o novo Role e usuario no Banco
        db.add(db_role)
        db.add(db_user)
        db.commit()

        # Garante o dado mais recente
        db.refresh(db_role)
        db.refresh(db_user)

        #LOG do cadastros
        logger.info(f"Usuário {db_user.username} criado com Sucesso com a role {user_in.role}.")        

        # Retorna os dados como Pydantic (convertendo o objeto SQLAlchemy)
        # Conversão usando from_orm
        # return db_user        
        return {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "role": db_role.role_type.value,
            "is_active": db_user.is_active,
            "is_admin": db_user.is_admin
        }

    except Exception as e:
        logger.error(f"Erro ao criar o usuário {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar o Usuario"
        )
