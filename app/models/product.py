from sqlalchemy import Boolean, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column("ProductID", Integer, primary_key=True)
    category_id: Mapped[int] = mapped_column("CategoryID", Integer)
    supplier_id: Mapped[int | None] = mapped_column("SupplierID", Integer, nullable=True)
    name: Mapped[str] = mapped_column("ProductName", String(200), index=True)
    brand: Mapped[str | None] = mapped_column("Brand", String(100), nullable=True)
    model: Mapped[str | None] = mapped_column("Model", String(100), nullable=True)
    description: Mapped[str | None] = mapped_column("Description", String(1000), nullable=True)
    price: Mapped[float] = mapped_column("Price", Float)
    stock_quantity: Mapped[int] = mapped_column("StockQuantity", Integer, default=0)
    warranty_months: Mapped[int] = mapped_column("WarrantyMonths", Integer, default=12)
    is_active: Mapped[bool] = mapped_column("IsActive", Boolean, default=True)
