from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.config import DATABASE_URL
from app.models.user import DBUser, DBRole
from app.auth.security import hash_password
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

# Cria a engine do SQLAlchemy, interface para o BD
engine = create_engine(DATABASE_URL) 

# Cria um "fabrica de sessoes", serve para realizar as operações (consulta, inserções, atualizações)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criação da Classe base para todos os modelos
Base = declarative_base()

def seed_adimin(db: Session):
    '''Cria um usuario ADMIN, caso não exista no Banco'''
    admin_email = "admin@email.com"
    existing_admin = db.query(DBUser).filter(DBUser.email == admin_email).first()

    if not existing_admin:
        try:
            db_admin = DBUser(
                username = 'Admin',
                email = admin_email,
                password = hash_password('admin1234'),
                is_admin = True                    
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

            #LOG do cadastros
            logger.info(f"Usuário {db_admin.username} criado com Sucesso com a role {db_role_admin.role}.")        
        except Exception as e:
            logger.error(f"Erro ao criar o usuário admin{e}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao criar o Usuario ADMIN"
            )


# para fornecer a sessão para cada requisição ao banco, para gerenciar as conexões ao banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# serve para criar as tabelas no banco
def create_all():
    Base.metadata.create_all(bind=engine)
    
    