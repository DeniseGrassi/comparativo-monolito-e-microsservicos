from pydantic import BaseModel, ConfigDict


class OrderCreate(BaseModel):
    customer_id: int
    product_id: int
    quantity: int


class Order(OrderCreate):
    id: int
    total_price: float

    model_config = ConfigDict(from_attributes=True)