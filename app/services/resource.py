from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import resource as resource_repositories
from app.schemas.resource import ResourceCreate, ResourceOut

def register_resource(db: Session, resource_in: ResourceCreate) -> ResourceOut:
    """Cria um novo recursos no banco de dados"""
    return resource_repositories.create_resource(db, resource_in)