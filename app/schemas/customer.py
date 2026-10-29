from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CustomerCreate(BaseModel):
    name: str = Field(min_length=1, max_length=201)
    balance: float = Field(default=0, ge=0)
    role: Literal["buyer", "seller"]


class CustomerRead(CustomerCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
