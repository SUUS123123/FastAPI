from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.models.product import Product
from app.models.purchase import Purchase


def create(db: Session, **values: object) -> Product:
    product = Product(**values)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_all(db: Session) -> list[Product]:
    return list(db.scalars(select(Product).order_by(Product.id)))


def search(
    db: Session,
    *,
    name: str | None = None,
    category_id: int | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> list[Product]:
    query = select(Product)

    if name:
        query = query.where(Product.name.ilike(f"%{name.strip()}%"))
    if category_id is not None:
        query = query.where(Product.category_id == category_id)
    if category:
        query = query.join(Category, Product.category_id == Category.id)
        query = query.where(Category.name.ilike(f"%{category.strip()}%"))
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)

    return list(db.scalars(query.order_by(Product.id)))


def get_by_id(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)


def has_purchases(db: Session, product_id: int) -> bool:
    purchase_id = db.scalar(
        select(Purchase.id).where(Purchase.product_id == product_id).limit(1)
    )
    return purchase_id is not None


def delete(db: Session, product: Product) -> None:
    db.delete(product)
    db.commit()
