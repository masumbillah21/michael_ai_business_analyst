from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=True)
    price = Column(Float, nullable=False)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Sale(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    sold_at = Column(DateTime, default=datetime.datetime.utcnow)

    product = relationship("Product")
    customer = relationship("Customer")

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    user_question = Column(Text, nullable=False)
    generated_sql = Column(Text)
    result_json = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def get_engine(sqlite_path="sqlite:///michael.db"):
    return create_engine(sqlite_path, future=True)

def get_session(engine):
    Session = sessionmaker(bind=engine, future=True)
    return Session()
