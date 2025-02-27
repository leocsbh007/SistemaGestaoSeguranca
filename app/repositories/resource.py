from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.resource import DBResource
from app.schemas.resource import ResourceCreate, ResourceOut, ResourceType
from app.auth import security
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

def create_resource(db: Session, resource_in: ResourceCreate) -> DBResource:

    try:        
        try:
            resource_in.type = ResourceType(resource_in.type)  # Converte a string para enum
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Tipo inválido: {resource_in.type}. Deve ser um dos seguintes: {[r.value for r in ResourceType]}"
            )
        
        db_resource = DBResource(**resource_in.dict())
        db.add(db_resource)
        db.commit()
        db.refresh(db_resource)

        #LOG do cadastros
        logger.info(f"Recurso {db_resource.name} criado com Sucesso!")        
        
        return db_resource

    except Exception as e:
        logger.error(f"Erro ao criar o Recurso {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar o Recuso"
        )