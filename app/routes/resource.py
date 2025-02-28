from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.base import get_db
from app.services.resource import register_resource
from app.models import resource as resource_db
from app.schemas.resource import ResourceIn, ResourceOut
from app.repositories import resource as resource_repositories
from app.auth.middleware import get_current_user, require_admin

router = APIRouter()

@router.post("/resources/", response_model=ResourceOut, dependencies=[Depends(require_admin)], status_code=status.HTTP_201_CREATED)
def create_resource(resource_in: ResourceIn, db: Session = Depends(get_db)):

    if resource_in.asset_number is None or resource_in.name is None or resource_in.type is None or resource_in.description is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Os campos 'Patrimônio', 'nome', 'tipo' e 'descrição' são obrigatórios"
        )

    return register_resource(db, resource_in)


@router.get("/resources/", response_model=List[ResourceOut], dependencies=[Depends(get_current_user)])
def get_resources(db: Session = Depends(get_db)):

    resources = db.query(resource_db.DBResource).all()
    
    if resources is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Recurso não encontrado"
            )
    
    resources_out = []
    # Garantindo que os valores de 'type' e 'status' sejam strings
    for resource in resources:
        resource_out = ResourceOut(
            id=resource.id,
            asset_number=resource.asset_number,
            name=resource.name,
            type=resource.type.value,  # Convertendo o enum para string
            description=resource.description,
            status=resource.status.value  # Convertendo o enum para string
        )
        resources_out.append(resource_out)
    return resources_out



@router.get("/resources/{resource_id}", response_model=ResourceOut, dependencies=[Depends(get_current_user)])
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(resource_db.DBResource).filter(resource_db.DBResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    return resource

@router.put("/resources/{resource_id}", response_model=ResourceOut, dependencies=[Depends(require_admin)])
def update_resource(resource_id: int, resource_in: ResourceIn, db: Session = Depends(get_db)):
    db_resource = resource_repositories.get_resource_by_id(db, resource_id)
    if db_resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recurso não encontrado"
        )
    
    exist_resource_asset_number = resource_repositories.get_resource_by_asset_number(db, resource_in.asset_number)
    if exist_resource_asset_number is not None and exist_resource_asset_number.id != db_resource.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O recurso já existe com esse número de patrimônio"
        )
    
    exist_resource_name = resource_repositories.get_resource_by_name(db, resource_in.name)
    if exist_resource_name is not None and exist_resource_name.id != db_resource.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O recurso já existe com esse nome"
        )


    for key, value in resource_in.dict(exclude_unset=True).items():
        setattr(db_resource, key, value)
    try:
        db.commit()        
        db.refresh(db_resource)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar o recurso no banco de dados"
        )
    return ResourceOut(
            id=db_resource.id,
            asset_number=db_resource.asset_number,
            name=db_resource.name,
            type=db_resource.type.value,
            description=db_resource.description,
            status=db_resource.status.value
        )


@router.delete("/resources/{resource_id}", dependencies=[Depends(require_admin)])
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(resource_db.DBResource).filter(resource_db.DBResource.id == resource_id).first()    

    if not resource:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recurso não encontrado")

    db.delete(resource)
    db.commit()
    return {"detail": "Recurso deletado com sucesso"}