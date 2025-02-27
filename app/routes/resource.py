from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.base import get_db
from app.services.resource import register_resource
from app.models import resource as resource_db
from app.schemas.resource import ResourceCreate, ResourceOut, ResourceUpdate
from app.auth.middleware import get_current_user, require_admin

router = APIRouter()

@router.post("/resources/", response_model=ResourceOut, dependencies=[Depends(require_admin)], status_code=status.HTTP_201_CREATED)
def create_resource(resource_in: ResourceCreate, db: Session = Depends(get_db)):
    if resource_in.name is None or resource_in.type is None or resource_in.description is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Os campos 'nome', 'tipo' e 'descrição' são obrigatórios"
        )
    print(f'Recurso Create Nome: {resource_in.name}')
    print(f'Recurso Create Tipo: {resource_in.type}')
    print(f'Recurso Create Descrição: {resource_in.description}')
    print(f'Recurso Create Status: {resource_in.status}')
    try:
        return register_resource(db, resource_in)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar o Usuario, usuário já existe"
        )  

@router.get("/resources/", response_model=List[ResourceOut], dependencies=[Depends(get_current_user)])
def get_resources(db: Session = Depends(get_db)):

    resources = db.query(resource_db.DBResource).all()

    
    if register_resource is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
            )
    
    resources_out = []
    # Garantindo que os valores de 'type' e 'status' sejam strings
    for resource in resources:
        resource_out = ResourceUpdate(
            id=resource.id,
            name=resource.name,
            type=resource.type.value,  # Convertendo o enum para string
            description=resource.description,
            status=resource.status.value,  # Convertendo o enum para string
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
def update_resource(resource_id: int, resource_update: ResourceUpdate, db: Session = Depends(get_db)):
    resource = db.query(resource_db.DBResource).filter(resource_db.DBResource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    for key, value in resource_update.dict(exclude_unset=True).items():
        setattr(resource, key, value)
    db.commit()
    db.refresh(resource)
    return resource


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