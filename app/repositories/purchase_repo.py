from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.purchase import Purchase


def create(db: Session, *, product_id: int, buyer_id: int, seller_id: int, amount: float) -> Purchase:
    purchase = Purchase(
        product_id=product_id, buyer_id=buyer_id, seller_id=seller_id, amount=amount
    )
    db.add(purchase)
    return purchase


def get_all(db: Session) -> list[Purchase]:
    return list(db.scalars(select(Purchase).order_by(Purchase.id.desc())))
