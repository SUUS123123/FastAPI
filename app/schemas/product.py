from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    brand: str | None = Field(default=None, max_length=100)
    model: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=1000)
    price: float = Field(ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    category_id: int = Field(gt=0)
    supplier_id: int | None = None
    warranty_months: int = Field(default=12, ge=0)
    is_active: bool = True


class ProductRead(ProductCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
