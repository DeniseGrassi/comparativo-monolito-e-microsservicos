from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class Product(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)