from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer


def create(db: Session, *, first_name: str, last_name: str, balance: float, role: str) -> Customer:
    customer = Customer(
        first_name=first_name, last_name=last_name, balance=balance, role=role
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_all(db: Session) -> list[Customer]:
    return list(db.scalars(select(Customer).order_by(Customer.id)))


def get_by_id(db: Session, customer_id: int) -> Customer | None:
    return db.get(Customer, customer_id)
