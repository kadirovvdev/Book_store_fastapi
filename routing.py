from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas import Product, ProductCreate, Order, OrderCreate
from crud import create_product, get_products, get_product, create_order, get_orders, get_order

router = APIRouter()

@router.post("/products/", response_model=Product)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db=db, product=product)

@router.get("/products/", response_model=list[Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = get_products(db, skip=skip, limit=limit)
    return products

@router.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.post("/orders/", response_model=Order)
def create_new_order(order: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db=db, order=order)

@router.get("/orders/", response_model=list[Order])
def read_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    orders = get_orders(db, skip=skip, limit=limit)
    return orders

@router.get("/orders/{order_id}", response_model=Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order
