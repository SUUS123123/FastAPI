from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.customer import Customer
from app.repositories import customer_repo
from app.schemas.customer import CustomerCreate, CustomerRead
from app.services.customer_service import create_customer as create_customer_service

router = APIRouter(prefix="/customers", tags=["Покупатели"])


@router.post("", response_model=CustomerRead)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)) -> Customer:
    return create_customer_service(
        db, name=data.name, balance=data.balance, role=data.role
    )


@router.get("", response_model=list[CustomerRead])
def get_customers(db: Session = Depends(get_db)) -> list[Customer]:
    return customer_repo.get_all(db)
