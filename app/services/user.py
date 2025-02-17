from sqlalchemy.orm import Session
from app.repositories import user as user_repositories
from app.schemas.user import UserIn, UserOut

def register_user(db: Session, user_in: UserIn) -> UserOut:
    """Cria um novo usuario e verifica se o usuario já existe"""
    if user_repositories.get_user_by_email(db, user_in.email):
        raise ValueError("Usuario já existe")        
        
    return user_repositories.create_user(db, user_in)