from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models.loan import DBLoan
from app.schemas.loan import LoanIn, LoanStatus, LoanOut
from app.models.resource import DBResource, StatusType
from datetime import timedelta
import logging

# Configuração de Logger para log
logger = logging.getLogger(__name__)

def get_loan_by_resource_id(db: Session, resource_id: int) -> DBLoan | None:    
    response = db.query(DBLoan).filter(DBLoan.resource_id == resource_id).first()
    return response

def get_loan_by_loan_id(db: Session, loan_id: int) -> DBLoan | None:    
    response = db.query(DBLoan).filter(DBLoan.id == loan_id).first()
    return response

def create_loan(db: Session, loan_in: LoanIn) -> LoanOut:
    try:               
        resource_db = db.query(DBResource).filter(DBResource.id == loan_in.resource_id).first()
        if not resource_db or not resource_db.status != 'DISPONIVEL':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Recurso não esta disponivel para emprestimo"
            ) 

        # Atualiza o tempo de emprestimo        
        calculated_end_date = loan_in.start_date + timedelta(hours=loan_in.loan_duration_hours)

        db_loan = DBLoan(
        user_id=loan_in.user_id,
        resource_id=loan_in.resource_id,
        start_date=loan_in.start_date,
        end_date=calculated_end_date,
        status=LoanStatus.ATIVO
        )        
        resource_db.status = StatusType.EM_USO
         
        db.add(db_loan)
        db.commit()        
        db.refresh(db_loan)
        db.refresh(resource_db)

        #LOG do cadastros
        logger.info(f"Emprestimo do {resource_db.name} criado com Sucesso!")                

        return LoanOut(
            id=db_loan.id,
            user_id=db_loan.user_id,
            resource_id=db_loan.resource_id,
            start_date=db_loan.start_date,
            status=db_loan.status.value,
            calculated_end_date=db_loan.end_date
        )

    except Exception as e:
        logger.error(f"Erro ao criar o registro de Emprestimo {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar o registro de Emprestimo"
        )