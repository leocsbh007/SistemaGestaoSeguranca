from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories import loan as loan_repositories
from app.schemas.loan import LoanIn, LoanOut

def register_loan(db: Session, loan_in: LoanIn) -> LoanOut:    
    if loan_repositories.get_loan_by_resource_id(db, loan_in.resource_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O recurso já esta emprestado"
        )
    
    # if resource_repositories.get_resource_by_name(db, resource_in.name):
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="O recurso já existe com esse nome"
    #     )
    return loan_repositories.create_loan(db, loan_in)