from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.exc import IntegrityError
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
def get_products(
    name: str | None = Query(default=None, min_length=1),
    category: str | None = Query(default=None, min_length=1),
    category_id: int | None = Query(default=None, gt=0),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    db: Session = Depends(get_db),
) -> list[Product]:
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=422,
            detail="Минимальная цена не может быть больше максимальной",
        )
    return product_repo.search(
        db,
        name=name,
        category=category,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
    )


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    product = product_repo.get_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> Response:
    product = product_repo.get_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Товар не найден")
    if product_repo.has_purchases(db, product_id):
        raise HTTPException(
            status_code=409,
            detail="Нельзя удалить товар: он есть в истории покупок",
        )

    try:
        product_repo.delete(db, product)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Нельзя удалить товар: он есть в истории покупок",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
