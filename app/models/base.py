from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

# Cria a engine do SQLAlchemy, interface para o BD
engine = create_engine(DATABASE_URL) 

# Cria um "fabrica de sessoes", serve para realizar as operações (consulta, inserções, atualizações)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criação da Classe base para todos os modelos
Base = declarative_base()

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
    
    