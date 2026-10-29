from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


def create(db: Session, **values: object) -> Product:
    product = Product(**values)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_all(db: Session) -> list[Product]:
    return list(db.scalars(select(Product).order_by(Product.id)))


def get_by_id(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)
