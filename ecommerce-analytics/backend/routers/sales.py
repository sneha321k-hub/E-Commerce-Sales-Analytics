from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import get_db
from models import Order, OrderItem, Customer
from routers.auth import get_current_user
from schemas import SalesKPIs, TrendPoint, ChannelStat, OrderStatusStat

router = APIRouter()

EXCLUDED_STATUSES = ["cancelled"]


@router.get("/kpis", response_model=SalesKPIs)
def get_sales_kpis(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    # Revenue: sum(qty * unit_price) - sum(discount) for non-cancelled orders
    row = db.execute(
        select(
            func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), 0.0).label("gross"),
            func.coalesce(func.sum(Order.discount_amount), 0.0).label("discounts"),
            func.count(func.distinct(Order.id)).label("total_orders"),
        )
        .select_from(OrderItem)
        .join(Order, OrderItem.order_id == Order.id)
        .where(~Order.status.in_(EXCLUDED_STATUSES))
    ).one()

    revenue = float(row.gross) - float(row.discounts)
    total_orders = row.total_orders
    aov = revenue / total_orders if total_orders else 0.0
    total_customers = db.execute(select(func.count(Customer.id))).scalar_one()

    return SalesKPIs(
        total_revenue=round(revenue, 2),
        total_orders=total_orders,
        average_order_value=round(aov, 2),
        total_customers=total_customers,
    )


@router.get("/trend", response_model=List[TrendPoint])
def get_sales_trend(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    cutoff = datetime.utcnow() - timedelta(days=days)

    rows = db.execute(
        select(
            func.date(Order.created_at).label("date"),
            (
                func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), 0.0)
                - func.coalesce(func.sum(Order.discount_amount), 0.0)
            ).label("revenue"),
            func.count(func.distinct(Order.id)).label("orders"),
        )
        .select_from(Order)
        .join(OrderItem, OrderItem.order_id == Order.id)
        .where(
            Order.created_at >= cutoff,
            ~Order.status.in_(EXCLUDED_STATUSES),
        )
        .group_by(func.date(Order.created_at))
        .order_by(func.date(Order.created_at))
    ).all()

    return [
        TrendPoint(date=str(r.date), revenue=round(float(r.revenue), 2), orders=r.orders)
        for r in rows
    ]


@router.get("/by-channel", response_model=List[ChannelStat])
def get_sales_by_channel(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    rows = db.execute(
        select(
            Order.channel,
            (
                func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), 0.0)
                - func.coalesce(func.sum(Order.discount_amount), 0.0)
            ).label("revenue"),
            func.count(func.distinct(Order.id)).label("orders"),
        )
        .select_from(Order)
        .join(OrderItem, OrderItem.order_id == Order.id)
        .where(~Order.status.in_(EXCLUDED_STATUSES))
        .group_by(Order.channel)
    ).all()

    return [
        ChannelStat(channel=r.channel, revenue=round(float(r.revenue), 2), orders=r.orders)
        for r in rows
    ]


@router.get("/order-status", response_model=List[OrderStatusStat])
def get_order_status(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    rows = db.execute(
        select(Order.status, func.count(Order.id).label("count"))
        .group_by(Order.status)
    ).all()

    return [OrderStatusStat(status=r.status, count=r.count) for r in rows]
