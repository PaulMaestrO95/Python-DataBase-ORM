from datetime import datetime

import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)


class Book(Base):
    __tablename__ = 'book'

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=60), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id", ondelete="CASCADE"))

    publishers = relationship(Publisher, backref="books")


class Shop(Base):
    __tablename__ = 'shop'

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=60), unique=True)


class Stock(Base):
    __tablename__ = 'stock'

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id", ondelete="CASCADE"))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id", ondelete="CASCADE"))
    count = sq.Column(sq.Integer)

    books = relationship(Book, backref="stocks")
    shops = relationship(Shop, backref="stocks")


class Sale(Base):
    __tablename__ = 'sale'

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.NUMERIC(10, 2), nullable=False)
    date_sale = sq.Column(sq.DateTime, default=datetime.now)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id", ondelete="CASCADE"))
    count = sq.Column(sq.Integer)

    stocks = relationship(Stock, backref="sales")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
