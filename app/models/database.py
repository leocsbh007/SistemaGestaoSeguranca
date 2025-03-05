from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import DBUser, DBRole
from app.auth.security import hash_password
from app.models.base import get_db
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

def seed_admin(db: Session):
    '''Cria um usuario ADMIN, caso não exista no Banco'''
    admin_email = "admin@email.com"
    existing_admin = db.query(DBUser).filter(DBUser.email == admin_email).first()

    if not existing_admin:
        try:
            db_admin = DBUser(
                username='Admin',
                email=admin_email,
                hashed_password=hash_password('admin1234'),
                is_admin=True                    
            )
            db_role_admin = DBRole(
                role_type='ADMIN',
                user=db_admin
            )

            # Adiciona o novo Role no Banco
            db.add(db_role_admin)

            # Adiciona o novo Usuario no Banco
            db.add(db_admin)
            db.commit()
            db.refresh(db_admin)

            # LOG do cadastro
            logger.info(f"Usuário {db_admin.username} criado com sucesso com a role {db_role_admin.role_type}.")        
        except Exception as e:
            logger.error(f"Erro ao criar o usuário admin: {e}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar o Usuario ADMIN"
            )

def initialize_admin():
    '''Executa seed_admin ao iniciar o sistema'''
    #from app.models.database import get_db  # Importação dentro da função para evitar importação circular

    with next(get_db()) as db:
        seed_admin(db)
