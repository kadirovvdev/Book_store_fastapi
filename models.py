from sqlalchemy import Column, String, BigInteger, ForeignKey, Table, Float
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

Base = declarative_base()

book_author = Table(
    'book_author',
    Base.metadata,
    Column('author_id', BigInteger, ForeignKey('author.id'), primary_key=True),
    Column('book_id', BigInteger, ForeignKey('books.id'), primary_key=True)
)



class Author(Base):
    __tablename__ = 'author'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    year = Column(String, nullable=False)

    books = relationship('Books', secondary=book_author, back_populates='authors')


class BooksCategory(Base):
    __tablename__ = 'books_category'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Books(Base):
    __tablename__ = 'books'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    ISBN = Column(String, nullable=False)
    price = Column(BigInteger, nullable=False)
    image = Column(String, nullable=False)
    year = Column(BigInteger, nullable=False)
    book_category_id = Column(BigInteger, ForeignKey('books_category.id'))

    authors = relationship('Author', secondary=book_author, back_populates='books')
    reviews = relationship('Review', back_populates='book')
    category = relationship('BooksCategory')


class Review(Base):
    __tablename__ = 'review'

    id = Column(BigInteger, primary_key=True, index=True)
    comment = Column(String, nullable=False)
    star_given = Column(BigInteger, nullable=False)
    user = Column(BigInteger, nullable=False)
    book_id = Column(BigInteger, ForeignKey('books.id'))

    book = relationship('Books', back_populates='reviews')




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('books.id'))
    quantity = Column(Integer)
    total_price = Column(Float)

    product = relationship("Books",)