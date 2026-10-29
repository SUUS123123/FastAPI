from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


def create(db: Session, name: str) -> Category:
    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_all(db: Session) -> list[Category]:
    return list(db.scalars(select(Category).order_by(Category.id)))


def get_by_id(db: Session, category_id: int) -> Category | None:
    return db.get(Category, category_id)
