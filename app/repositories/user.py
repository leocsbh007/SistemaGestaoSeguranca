from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.user import User as DBUser
from app.schemas.user import UserCreate as UserCreateSchema

def create_user(db: Session, user_data: UserCreateSchema) -> DBUser:

    try:
        #verifica se o usuario já existe com o mesmo nome
        db_user = db.query(DBUser).filter(DBUser.username == user_data.username).first()
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
