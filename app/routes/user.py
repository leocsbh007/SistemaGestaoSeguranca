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
    
    try:
        #veifica se o usuario já existe com o mesmo nome
        db_user = db.query(user_db.User).filter(user_db.User.username == user_data.username).first()
        # print(f'Role: {db_user}')

        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario já registrado!!!")
        
        # Criptografa a senha do usuario
        hashed_password = auth.hash_password(user_data.password)
        # print(f'Hashed Password {hashed_password}')

        # Cria um novo objeto
        new_user = user_db.User(username=user_data.username, hashed_password=hashed_password, email=user_data.email)

        # Adiciona um role especifica
        new_role = user_db.Role(role_type=user_data.role, user=new_user)
        print(f'Role: {new_role.role_type}')

        # Converte para maiusculo, pois em minusculo estava dando erro no Banco
        new_role.role_type = new_role.role_type.upper()
        if new_role.role_type == 'ADMIN':            
            new_user.is_admin = True
        db.add(new_role)

        #Adiciona o novo Usuario
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        #LOG do cadastros
        logger.info(f"Usuário {new_user.username} criado com Sucesso com a role {user_data.role}.")

        # Retorna os dados como Pydantic (convertendo o objeto SQLAlchemy)
        # Conversão usando from_orm
        return schema_user.User.from_orm(new_user)
        #return {'Usuario Cadastrado com Sucesso'}
    except Exception as e:
        logger.error(f"Erro ao criar o usuário {e}")
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro ao criar o Usuario, usuário já existe")
    
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


    