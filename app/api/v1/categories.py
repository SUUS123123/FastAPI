from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.category import Category
from app.repositories import category_repo
from app.schemas.category import CategoryCreate, CategoryRead

router = APIRouter(prefix="/categories", tags=["Категории"])


@router.post("", response_model=CategoryRead)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)) -> Category:
    return category_repo.create(db, data.name)


@router.get("", response_model=list[CategoryRead])
def get_categories(db: Session = Depends(get_db)) -> list[Category]:
    return category_repo.get_all(db)
