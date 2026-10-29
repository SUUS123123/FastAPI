from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.purchase import Purchase
from app.repositories import purchase_repo
from app.schemas.purchase import PurchaseRead, PurchaseRequest
from app.services.purchase_service import purchase_product as purchase_product_service

router = APIRouter(tags=["Покупки"])


@router.post("/products/{product_id}/purchase", response_model=PurchaseRead, status_code=201)
def purchase_product(
    product_id: int, data: PurchaseRequest, db: Session = Depends(get_db)
) -> Purchase:
    return purchase_product_service(
        db,
        product_id=product_id,
        buyer_id=data.buyer_id,
        seller_id=data.seller_id,
        quantity=data.quantity,
    )


@router.get("/purchases", response_model=list[PurchaseRead])
def get_purchases(db: Session = Depends(get_db)) -> list[Purchase]:
    return purchase_repo.get_all(db)
