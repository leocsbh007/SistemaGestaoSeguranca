from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload
from app.models.base import get_db
from app.models import user as user_db
from app.schemas.user import UserIn, UserOut, RoleType
from app.services.user import register_user
from app.auth.middleware import require_admin, get_current_user
from app.repositories import user as user_repositories
from app.auth import security
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

# Cria um roteador para a rota de usuarios
router = APIRouter()

# Rota para listar todos os usuarios
@router.get("/users/", response_model=list[UserOut], dependencies=[Depends(get_current_user)])
def get_users(db: Session = Depends(get_db)):
    '''Rota para listar todos os usuarios, inclui a Role do Usuario'''
    users = db.query(user_db.DBUser).options(joinedload(user_db.DBUser.role)).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum usuário encontrado"
            )

    user_outs = []
    for user in users:
        user_out = UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            role=user.role.role_type.value if user.role else user_db.RoleType.FUNCIONARIO
        )
        user_outs.append(user_out)
    return user_outs     
    
@router.get("/users/{user_id}", response_model=UserOut, dependencies=[Depends(get_current_user)])
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserOut:
    '''Rota para buscar um usuario pelo ID'''
    db_user = db.query(user_db.DBUser).filter(user_db.DBUser.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario não encontrado"
        )
    return UserOut(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        is_admin=db_user.is_admin,
        role_type=db_user.role
    )

@router.post("/users/", response_model= UserOut, dependencies=[Depends(require_admin)], status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserIn, db: Session = Depends(get_db)):
    if user_in.email is None or user_in.username is None or user_in.password is None or user_in.role is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Os campos 'email', 'username', 'password' e 'role' são obrigatórios"
    )

    try:
        return register_user(db, user_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar o Usuario, usuário já existe"
        )    
    
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

@router.put("/users/{user_id_put}", response_model=UserOut, dependencies=[Depends(require_admin)])
def update_user(user_id_put: int, user_in: UserIn, db: Session = Depends(get_db)):
    '''Rota para atualizar um usuario'''  
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
    
    # Verifica se a senha não veio nula
    if user_in.password:
        hashed_password_in = security.hash_password(user_in.password)
    else:        
        hashed_password_in = db_user.hashed_password

    # Atualiza os campos para inserir no Banco
    # for key, value in user_in.dict(exclude_unset=True).items():
    #     setattr(db_user, key, value)

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
    
    # Valida se a role fornecida é válida antes de atualizar
    try:
        new_role = RoleType(user_in.role)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role inválida: {user_in.role}. Deve ser um dos seguintes: {[r.value for r in RoleType]}"
        )

    # Atualiza a role se necessário
    if db_role.role_type != new_role:
        db_role.role_type = new_role   

   # Verifica se o usuário deve ser admin
    db_user.is_admin = new_role == RoleType.ADMIN
    
    # Adiciona o novo Role no Banco
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Erro ao atualizar o usuário no banco de dados"
        )

    # Retorna os dados no formato esperado pelo UserOut
    return UserOut(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        is_admin=db_user.is_admin,
        role=new_role.value
    )
    
    
    

    


    