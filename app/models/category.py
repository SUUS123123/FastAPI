from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column("CategoryID", Integer, primary_key=True)
    name: Mapped[str] = mapped_column(
        "CategoryName", String(100), unique=True, index=True
    )
