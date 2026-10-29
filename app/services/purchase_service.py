from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.product import Product
from app.models.purchase import Purchase
from app.repositories import customer_repo, product_repo, purchase_repo


def purchase_product(
    db: Session, *, product_id: int, buyer_id: int, seller_id: int, quantity: int
) -> Purchase:
    buyer = customer_repo.get_by_id(db, buyer_id)
    seller = customer_repo.get_by_id(db, seller_id)
    product = product_repo.get_by_id(db, product_id)
    if buyer is None or seller is None:
        raise HTTPException(status_code=404, detail="Покупатель или продавец не найден")
    if product is None or not product.is_active:
        raise HTTPException(status_code=404, detail="Товар не найден")
    if buyer.id == seller.id:
        raise HTTPException(status_code=422, detail="Покупатель и продавец должны быть разными")
    if buyer.role != "buyer" or seller.role != "seller":
        raise HTTPException(status_code=422, detail="Проверьте роли покупателя и продавца")

    total = product.price * quantity
    try:
        debit = db.execute(
            update(Customer)
            .where(Customer.id == buyer.id, Customer.balance >= total)
            .values(balance=Customer.balance - total)
        )
        if debit.rowcount != 1:
            raise HTTPException(status_code=400, detail="Недостаточно денег на балансе покупателя")

        stock_update = db.execute(
            update(Product)
            .where(Product.id == product.id, Product.stock_quantity >= quantity)
            .values(stock_quantity=Product.stock_quantity - quantity)
        )
        if stock_update.rowcount != 1:
            raise HTTPException(status_code=400, detail="Недостаточно товара на складе")

        db.execute(
            update(Customer)
            .where(Customer.id == seller.id)
            .values(balance=Customer.balance + total)
        )
        purchase = purchase_repo.create(
            db,
            product_id=product.id,
            buyer_id=buyer.id,
            seller_id=seller.id,
            amount=total,
        )
        db.commit()
    except Exception:
        db.rollback()
        raise

    db.refresh(purchase)
    return purchase
