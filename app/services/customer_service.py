from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.repositories import customer_repo


def create_customer(db: Session, *, name: str, balance: float, role: str) -> Customer:
    name_parts = name.strip().split(maxsplit=1)
    if not name_parts or not name_parts[0]:
        raise HTTPException(status_code=422, detail="Введите имя покупателя")
    return customer_repo.create(
        db,
        first_name=name_parts[0],
        last_name=name_parts[1] if len(name_parts) > 1 else "",
        balance=balance,
        role=role,
    )
