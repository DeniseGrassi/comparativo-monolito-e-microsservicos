from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CustomerModel, OrderModel, ProductModel
from app.schemas.order import Order, OrderCreate


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", response_model=Order, status_code=201)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):
    if order.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    customer = (
        db.query(CustomerModel)
        .filter(CustomerModel.id == order.customer_id)
        .first()
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    product = (
        db.query(ProductModel)
        .filter(ProductModel.id == order.product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if product.stock < order.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    total_price = product.price * order.quantity

    new_order = OrderModel(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price
    )

    product.stock -= order.quantity

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


@router.get("/", response_model=List[Order])
def list_orders(
    db: Session = Depends(get_db)
):
    return db.query(OrderModel).all()


@router.get("/{order_id}", response_model=Order)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(OrderModel)
        .filter(OrderModel.id == order_id)
        .first()
    )

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order