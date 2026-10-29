from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.product import Product
from app.repositories import category_repo, product_repo
from app.schemas.product import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["Товары"])


@router.post("", response_model=ProductRead)
def create_product(data: ProductCreate, db: Session = Depends(get_db)) -> Product:
    if category_repo.get_by_id(db, data.category_id) is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return product_repo.create(db, **data.model_dump())


@router.get("", response_model=list[ProductRead])
def get_products(db: Session = Depends(get_db)) -> list[Product]:
    return product_repo.get_all(db)


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    product = product_repo.get_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product
