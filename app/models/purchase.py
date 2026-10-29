from sqlalchemy import CheckConstraint, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Purchase(Base):
    __tablename__ = "purchases"
    __table_args__ = (CheckConstraint("BuyerID <> SellerID"),)

    id: Mapped[int] = mapped_column("PurchaseID", Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(
        "ProductID", ForeignKey("products.ProductID"), nullable=False
    )
    buyer_id: Mapped[int] = mapped_column(
        "BuyerID", ForeignKey("Customers.CustomerID"), nullable=False
    )
    seller_id: Mapped[int] = mapped_column(
        "SellerID", ForeignKey("Customers.CustomerID"), nullable=False
    )
    amount: Mapped[float] = mapped_column("Amount", Float, nullable=False)
