from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ProductModel
from app.schemas.product import Product, ProductCreate


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post("/", response_model=Product, status_code=201)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    new_product = ProductModel(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get("/", response_model=List[Product])
def list_products(
    db: Session = Depends(get_db)
):
    return db.query(ProductModel).all()


@router.get("/{product_id}", response_model=Product)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(ProductModel)
        .filter(ProductModel.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.patch("/{product_id}/stock", response_model=Product)
def update_stock(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(ProductModel)
        .filter(ProductModel.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    if product.stock < quantity:
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock"
        )

    product.stock -= quantity

    db.commit()
    db.refresh(product)

    return product