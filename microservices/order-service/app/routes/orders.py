from typing import List

import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import OrderModel
from app.schemas.order import Order, OrderCreate


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


import os

CUSTOMER_SERVICE_URL = os.getenv(
    "CUSTOMER_SERVICE_URL",
    "http://127.0.0.1:8002"
)

PRODUCT_SERVICE_URL = os.getenv(
    "PRODUCT_SERVICE_URL",
    "http://127.0.0.1:8001"
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

    try:
        customer_response = requests.get(
            f"{CUSTOMER_SERVICE_URL}/customers/{order.customer_id}",
            timeout=3
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Customer service unavailable"
        )

    if customer_response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if customer_response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Error communicating with customer service"
        )

    try:
        product_response = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{order.product_id}",
            timeout=3
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Product service unavailable"
        )

    if product_response.status_code == 404:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if product_response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Error communicating with product service"
        )

    product = product_response.json()

    if product["stock"] < order.quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    total_price = product["price"] * order.quantity

    try:
        stock_response = requests.patch(
            f"{PRODUCT_SERVICE_URL}/products/{order.product_id}/stock",
            params={"quantity": order.quantity},
            timeout=3
        )
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Product service unavailable while updating stock"
        )

    if stock_response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Error updating product stock"
        )

    new_order = OrderModel(
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        total_price=total_price
    )

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