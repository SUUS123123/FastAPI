from pydantic import BaseModel, Field


class PurchaseRequest(BaseModel):
    buyer_id: int = Field(gt=0)
    seller_id: int = Field(gt=0)
    quantity: int = Field(default=1, gt=0)


class PurchaseRead(BaseModel):
    id: int
    product_id: int
    buyer_id: int
    seller_id: int
    amount: float
