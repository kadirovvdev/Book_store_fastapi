from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from utils import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

from sqlalchemy.orm import Session
from models import Books, Order
from schemas import ProductCreate, OrderCreate

def get_product(db: Session, product_id: int):
    return db.query(Books).filter(Books.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Books).offset(skip).limit(limit).all()

def create_product(db: Session, product: ProductCreate):
    db_product = Books(name=product.name, description=product.description, price=product.price, quantity=product.quantity)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: OrderCreate):
    db_product = get_product(db, order.product_id)
    if db_product is None or db_product.quantity < order.quantity:
        raise HTTPException(status_code=400, detail="Product not available or insufficient quantity")

    db_product.quantity -= order.quantity
    total_price = db_product.price * order.quantity
    db_order = Order(product_id=order.product_id, quantity=order.quantity, total_price=total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order
