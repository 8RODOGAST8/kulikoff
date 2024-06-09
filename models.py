# -*- coding: UTF-8 -*-
from sqlalchemy import Column, Integer, Float, Date, DateTime, Text, Boolean, String, ForeignKey, or_, not_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, query_expression
from sqlalchemy.sql import func
from database import Base, db_session, engine as db_engine
import datetime
from flask_login import UserMixin
from eng import manager


class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    theProductSName = Column(String(100), unique=True, default=None)
    compositions = relationship("Composition", back_populates="ingredients")


class User(UserMixin, Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    password = Column(String(100), default=None)
    login = Column(String(100), unique=True, default=None)


class Composition(Base):
    __tablename__ = 'compositions'
    id = Column(Integer, primary_key=True)
    dish_id = Column(Integer, ForeignKey('dishs.id'), doc="Состав блюда")
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'), doc="Ингредиенты блюда")
    dishs = relationship("Dish", back_populates="compositions")
    ingredients = relationship("Ingredient", back_populates="compositions")
    weighingedients = Column(Integer, default=None)


class Namecategory(Base):
    __tablename__ = 'namecategories'
    id = Column(Integer, primary_key=True)
    category = Column(String(100), unique=True, default=None)
    dishs = relationship("Dish", back_populates="namecategories")


class Dish(Base):
    __tablename__ = 'dishs'
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey('namecategories.id'), doc="Категория блюда")
    nameOftheDish = Column(String(50), unique=True)
    cookingtime = Column(Integer)
    weightportions = Column(Integer)
    price = Column(Integer)
    image = Column(String(500), default=None)
    href = Column(String(100), default=None)
    namecategories = relationship("Namecategory", back_populates="dishs")
    compositions = relationship("Composition", back_populates="dishs")


class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    namerestaurant = Column(String(50), unique=True)
    telephonenumber = Column(String(12))
    email = Column(String(100))
    adress = Column(String(100))
    workingdays = Column(String(50))
    workinghours = Column(String(50))


class Tablereservation(Base):
    __tablename__ = 'tablereservations'
    id = Column(Integer, primary_key=True)
    fio = Column(String(100))
    telephonenumber = Column(String(12))
    numberOfGuests = Column(Integer)
    bookingDate = Column(DateTime[12])




def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from database import engine
    Base.metadata.create_all(bind=engine)
    db_session.commit()


def print_schema(table_class):
    from sqlalchemy.schema import CreateTable, CreateColumn
    print(str(CreateTable(table_class.__table__).compile(db_engine)))


def print_columns(table_class, *attrNames):
    from sqlalchemy.schema import CreateTable, CreateColumn
    c = table_class.__table__.c
    print(',\r\n'.join((str(CreateColumn(getattr(c, attrName)).compile(db_engine)) \
                        for attrName in attrNames if hasattr(c, attrName)
                        )))


if __name__ == "__main__":
    init_db()
