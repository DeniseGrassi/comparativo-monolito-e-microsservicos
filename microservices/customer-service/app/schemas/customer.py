from pydantic import BaseModel, ConfigDict


class CustomerCreate(BaseModel):
    name: str
    email: str


class Customer(CustomerCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)