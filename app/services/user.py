from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import user as user_repositories
from app.schemas.user import UserIn, UserOut

def register_user(db: Session, user_in: UserIn) -> UserOut:
    """Cria um novo usuario e verifica se o usuario já existe"""
    if user_repositories.get_user_by_email(db, user_in.email) is not None:
        print(f'User Email: {user_in.email}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Já existe um usuário com este email"
        ) 
    if user_repositories.get_user_by_username(db, user_in.username) is not None:
        print(f'User Username: {user_in.username}')
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Já existe um usuário com este username"
        )          
        
    return user_repositories.create_user(db, user_in)