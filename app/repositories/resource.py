from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.resource import DBResource
from app.schemas.resource import ResourceIn, ResourceOut
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

def get_resource_by_name(db: Session, name: str) -> DBResource | None:
    '''Retorna um usuario pelo nome'''
    response = db.query(DBResource).filter(DBResource.name == name).first()        
    return response

def get_resource_by_asset_number(db: Session, asset_number: str) -> DBResource | None:
    '''Retorna um usuario pelo nome'''
    response = db.query(DBResource).filter(DBResource.asset_number == asset_number).first()
    return response

def get_resource_by_id(db: Session, resource_id: int) -> DBResource | None:
    '''Retorna um recurso pelo id'''
    response = db.query(DBResource).filter(DBResource.id == resource_id).first()
    return response

def create_resource(db: Session, resource_in: ResourceIn) -> ResourceOut:

    try:        
        # Validação do tipo de recurso       
        db_resource = DBResource(**resource_in.dict())        
        db.add(db_resource)
        db.commit()        
        db.refresh(db_resource)

        #LOG do cadastros
        logger.info(f"Recurso {db_resource.name} criado com Sucesso!")                

        # return resource_out
        return ResourceOut(
            id = db_resource.id,
            asset_number = db_resource.asset_number,
            name = db_resource.name,
            type = db_resource.type.value,
            description = db_resource.description,
            status = db_resource.status.value,
        )

    except Exception as e:
        logger.error(f"Erro ao criar o Recurso {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar o Recuso"
        )