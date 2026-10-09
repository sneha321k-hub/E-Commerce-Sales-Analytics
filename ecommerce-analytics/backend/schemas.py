from typing import List, Optional
from pydantic import BaseModel


# ── Sales ──────────────────────────────────────────────────────────────────

class SalesKPIs(BaseModel):
    total_revenue: float
    total_orders: int
    average_order_value: float
    total_customers: int


class TrendPoint(BaseModel):
    date: str
    revenue: float
    orders: int


class ChannelStat(BaseModel):
    channel: str
    revenue: float
    orders: int


class OrderStatusStat(BaseModel):
    status: str
    count: int


# ── Products ───────────────────────────────────────────────────────────────

class TopProduct(BaseModel):
    product_id: int
    name: str
    category: str
    revenue: float
    units_sold: int


class CategoryStat(BaseModel):
    category: str
    revenue: float
    orders: int


class ProductReturnRate(BaseModel):
    product_id: int
    name: str
    category: str
    total_orders: int
    returned_orders: int
    return_rate: float


# ── Customers ──────────────────────────────────────────────────────────────

class CustomerSummary(BaseModel):
    total_customers: int
    new_this_month: int
    returning_customers: int


class TopCustomer(BaseModel):
    customer_id: int
    name: str
    email: str
    total_spend: float
    order_count: int


class CountryStat(BaseModel):
    country: str
    customer_count: int
    revenue: float


class NewVsReturningPoint(BaseModel):
    month: str
    new_customers: int
    returning_customers: int
