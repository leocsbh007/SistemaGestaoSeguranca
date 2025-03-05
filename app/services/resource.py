from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import resource as resource_repositories
from app.schemas.resource import ResourceIn, ResourceOut

def register_resource(db: Session, resource_in: ResourceIn) -> ResourceOut:
    """Cria um novo recursos no banco de dados"""    
    if resource_repositories.get_resource_by_asset_number(db, resource_in.asset_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O recurso já existe com esse número de patrimônio"
        )
    
    if resource_repositories.get_resource_by_name(db, resource_in.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O recurso já existe com esse nome"
        )
    return resource_repositories.create_resource(db, resource_in)