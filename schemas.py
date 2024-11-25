# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class OrderItemBase(BaseModel):
    display_name: str
    name: str
    default_code: str
    qty: float
    sales_cess_amount: float
    list_price: float
    mrp: float
    vat_percent: float


class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    display_name: str
    customer_name: str
    counter: str
    shop: str
    user: str
    amount_untaxed: float
    amount_tax: float
    total_cess: float
    amount_total: float
    payment_journal_id: int
    create_date: datetime


class OrderCreate(OrderBase):
    order_items: List[OrderItemBase]


class Order(OrderBase):
    id: int
    order_items: List[OrderItem]

    class Config:
        orm_mode = True