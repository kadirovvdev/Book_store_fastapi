# from fastapi import FastAPI, Depends, HTTPException
# from sqlalchemy.orm import Session
# import models, database, init_db
#
# app = FastAPI()
#
# def get_db():
#     db = database.SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
# @app.on_event("startup")
# def on_startup():
#     init_db.init_db(database.SessionLocal())
#
# @app.post("/authors/")
# def create_author(author: models.Author, db: Session = Depends(get_db)):
#     db.add(author)
#     db.commit()
#     db.refresh(author)
#     return author
#
# @app.post("/books/")
# def create_book(book: models.Books, db: Session = Depends(get_db)):
#     db.add(book)
#     db.commit()
#     db.refresh(book)
#     return book
#
# @app.post("/reviews/")
# def create_review(review: models.Review, db: Session = Depends(get_db)):
#     db.add(review)
#     db.commit()
#     db.refresh(review)
#     return review
#
# @app.get("/books/{book_id}")
# def get_book(book_id: int, db: Session = Depends(get_db)):
#     book = db.query(models.Books).filter(models.Books.id == book_id).first()
#     if book is None:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return book
#
from datetime import timedelta

# from fastapi import FastAPI, Depends
# from fastapi_users import FastAPIUsers, schemas, models
# from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
# from fastapi_users.db import SQLAlchemyUserDatabase
# from fastapi_users.manager import BaseUserManager, UUIDIDMixin
# from pydantic import BaseModel, EmailStr
#
# from sqlalchemy import Column, String
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
#
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"
# SECRET = "SECRET"
#
# Base = declarative_base()
#
# class User(models.BaseUser, models.BaseOAuthAccountMixin, Base):
#     __tablename__ = "users"
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=False)
#
# class UserCreate(schemas.BaseUserCreate):
#     first_name: str
#     last_name: str
#
# class UserUpdate(schemas.BaseUserUpdate):
#     first_name: str
#     last_name: str
#
# class UserDB(User, schemas.BaseUserDB):
#     pass
#
# engine = create_async_engine(DATABASE_URL, echo=True)
# async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
#
# async def get_user_db(session: AsyncSession = Depends(async_session_maker)):
#     yield SQLAlchemyUserDatabase(UserDB, session)
#
# class UserManager(UUIDIDMixin, BaseUserManager[UserDB, str]):
#     user_db_model = UserDB
#     reset_password_token_secret = SECRET
#     verification_token_secret = SECRET
#
#     async def on_after_register(self, user: UserDB, request=None):
#         print(f"User {user.id} has registered.")
#
#     async def on_after_forgot_password(self, user: UserDB, token: str, request=None):
#         print(f"User {user.id} has forgot their password. Reset token: {token}")
#
#     async def on_after_request_verify(self, user: UserDB, token: str, request=None):
#         print(f"Verification requested for user {user.id}. Verification token: {token}")
#
# async def get_user_manager(user_db=Depends(get_user_db)):
#     yield UserManager(user_db)
#
# app = FastAPI()
#
# bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
#
# def get_jwt_strategy() -> JWTStrategy:
#     return JWTStrategy(secret=SECRET, lifetime_seconds=3600)
#
# auth_backend = AuthenticationBackend(
#     name="jwt",
#     transport=bearer_transport,
#     get_strategy=get_jwt_strategy,
# )
#
# fastapi_users = FastAPIUsers[User, str](
#     get_user_manager,
#     [auth_backend],
# )
#
# app.include_router(
#     fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
# )
# app.include_router(
#     fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"]
# )
# app.include_router(
#     fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"]
# )
#
#
# class UserRead(BaseModel):
#     id: str
#     email: EmailStr
#     is_active: bool
#     is_superuser: bool
#     is_verified: bool
#
#
# app.include_router(
#     fastapi_users.get_verify_router(UserRead), prefix="/auth", tags=["auth"]
# )
#
# @app.on_event("startup")
# async def on_startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)


from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import engine, Base, get_db
from models import User
from schemas import UserCreate, UserOut
from crud import create_user, get_user_by_email
from auth import authenticate_user, create_access_token, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/signup", response_model=UserOut)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@app.post("/token", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user



