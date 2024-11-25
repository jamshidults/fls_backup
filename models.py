# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String)
    customer_name = Column(String)
    counter = Column(String)
    shop  = Column(String)
    user  = Column(String)
    amount_untaxed = Column(Float)
    amount_tax = Column(Float)
    total_cess = Column(Float)
    amount_total = Column(Float)
    create_date = Column(DateTime)
    payment_journal_id = Column(Integer)
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer)
    display_name = Column(String)
    name = Column(String)
    default_code = Column(String)
    qty = Column(Float)
    qty_available = Column(Float)
    sales_cess_amount = Column(Float)
    list_price = Column(Float)
    mrp = Column(Float)
    vat_percent = Column(Float)
    order = relationship("Order", back_populates="order_items")


