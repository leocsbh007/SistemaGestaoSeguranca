from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.base import get_db
from app.services.loan import register_loan
from app.models.resource import DBResource, StatusType
from app.models import loan as loan_db
from app.schemas.loan import LoanIn, LoanOut
from app.repositories import loan as loan_repositories
from app.auth.middleware import get_current_user, require_admin

router = APIRouter()

@router.get("/loans/", response_model=list[LoanOut], dependencies=[Depends(get_current_user)])
def get_loans(db: Session = Depends(get_db)):    
    db_loan = db.query(loan_db.DBLoan).all()    
    if not db_loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum emprestimo encontrado"
            )

    loan_outs = []
    for loan in db_loan:
        loan_out = LoanOut(
            id=loan.id,
            user_id=loan.user_id,
            resource_id=loan.resource_id,
            start_date=loan.start_date,
            status=loan.status.value,
            calculated_end_date=loan.end_date
        )        
        loan_outs.append(loan_out)
    return loan_outs

@router.get("/loans/{loan_id}", response_model=LoanOut, dependencies=[Depends(get_current_user)])
def get_loans(loan_id: int, db: Session = Depends(get_db)) -> LoanOut:
    db_loan = db.query(loan_db.DBLoan).filter(loan_db.DBLoan.id == loan_id).first()
    
    if not db_loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum emprestimo não encontrado"
    )

    return LoanOut(
            id=db_loan.id,
            user_id=db_loan.user_id,
            resource_id=db_loan.resource_id,
            start_date=db_loan.start_date,
            status=db_loan.status.value,
            calculated_end_date=db_loan.end_date
        )       


@router.post("/loans/", response_model=LoanOut, dependencies=[Depends(require_admin)], status_code=status.HTTP_201_CREATED)
def create_loan(loan_in: LoanIn, db: Session = Depends(get_db)) -> LoanOut:    
    if loan_in.user_id is None or loan_in.resource_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Os campos 'ID de Usuario', 'ID do Recurso' são obrigatórios"
    )    
    return register_loan(db, loan_in)  

@router.put("/loans/{loan_id}", response_model=LoanOut, dependencies=[Depends(require_admin)])
def update_resource(loan_id: int, loan_in: LoanIn, db: Session = Depends(get_db)) -> LoanOut:
    db_loan = loan_repositories.get_loan_by_loan_id(db, loan_id)     
    if not db_loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Emprestimo não encontrado"
        )
    
    # exist_resource_id = loan_repositories.get_loan_by_resource_id(db, loan_in.resource_id)
    # if exist_resource_id is not None and exist_resource_id.resource_id != db_loan.resource_id:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="O recurso já existe esta Emprestado"
    #     )
    
    # A unica coisa permitida para ser alterada é o status do emprestimo, pois o registro serve para relatorios futuros
    db_loan.status = loan_in.status
    try:
        db.commit()        
        db.refresh(db_loan)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar o recurso no banco de dados"
        )
    return LoanOut(
            id=db_loan.id,
            user_id=db_loan.user_id,
            resource_id=db_loan.resource_id,
            start_date=db_loan.start_date,
            status=db_loan.status.value,
            calculated_end_date=db_loan.end_date
        )

@router.delete("/loans/{loan_id}", dependencies=[Depends(require_admin)])
def delete_resource(loan_id: int, db: Session = Depends(get_db)) -> dict:
    db_loan = db.query(loan_db.DBLoan).filter(loan_db.DBLoan.id == loan_id).first()   
    if not db_loan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emprestimo não encontrado")
    
    resource_db = db.query(DBResource).filter(DBResource.id == db_loan.resource_id).first() 
    if not resource_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Recurso associado ao emprestimo não encontrado")
    
    resource_db.status = StatusType.DISPONIVEL
    db.delete(db_loan)
    db.commit()
    return {"detail": "Recurso deletado com sucesso"}