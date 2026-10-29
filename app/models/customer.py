from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Customer(Base):
    __tablename__ = "Customers"

    id: Mapped[int] = mapped_column("CustomerID", Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column("FirstName", String(100), nullable=False)
    last_name: Mapped[str] = mapped_column("LastName", String(100), nullable=False)
    balance: Mapped[float] = mapped_column("Balance", Float, nullable=False, default=0)
    role: Mapped[str] = mapped_column("Role", String(20), nullable=False, default="buyer")

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()
