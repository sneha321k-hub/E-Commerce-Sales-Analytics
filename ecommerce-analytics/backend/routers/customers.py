from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func, case, select, or_
from sqlalchemy.orm import Session

from database import get_db
from models import Order, OrderItem, Customer
from routers.auth import get_current_user
from schemas import CustomerSummary, TopCustomer, CountryStat, NewVsReturningPoint

router = APIRouter()


@router.get("/summary", response_model=CustomerSummary)
def get_customer_summary(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    total = db.execute(select(func.count(Customer.id))).scalar_one()

    now = datetime.utcnow()
    month_start = datetime(now.year, now.month, 1)

    # Subquery: first order date per customer
    first_order_subq = (
        select(
            Order.customer_id,
            func.min(Order.created_at).label("first_order"),
        )
        .group_by(Order.customer_id)
        .subquery()
    )

    new_this_month = db.execute(
        select(func.count())
        .select_from(first_order_subq)
        .where(first_order_subq.c.first_order >= month_start)
    ).scalar_one()

    returning = db.execute(
        select(func.count())
        .select_from(first_order_subq)
        .where(first_order_subq.c.first_order < month_start)
    ).scalar_one()

    return CustomerSummary(
        total_customers=total,
        new_this_month=new_this_month or 0,
        returning_customers=returning or 0,
    )


@router.get("/top", response_model=List[TopCustomer])
def get_top_customers(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    spend_expr = (
        func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), 0.0)
        - func.coalesce(func.sum(Order.discount_amount), 0.0)
    )

    rows = db.execute(
        select(
            Customer.id,
            Customer.name,
            Customer.email,
            spend_expr.label("total_spend"),
            func.count(func.distinct(Order.id)).label("order_count"),
        )
        .select_from(Customer)
        .join(Order, Order.customer_id == Customer.id)
        .join(OrderItem, OrderItem.order_id == Order.id)
        .where(~Order.status.in_(["cancelled"]))
        .group_by(Customer.id, Customer.name, Customer.email)
        .order_by(spend_expr.desc())
        .limit(10)
    ).all()

    return [
        TopCustomer(
            customer_id=r.id,
            name=r.name,
            email=r.email,
            total_spend=round(float(r.total_spend), 2),
            order_count=r.order_count,
        )
        for r in rows
    ]


@router.get("/by-country", response_model=List[CountryStat])
def get_customers_by_country(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    rows = db.execute(
        select(
            Customer.country,
            func.count(func.distinct(Customer.id)).label("customer_count"),
            func.coalesce(
                func.sum(OrderItem.quantity * OrderItem.unit_price)
                - func.sum(Order.discount_amount),
                0.0,
            ).label("revenue"),
        )
        .select_from(Customer)
        .outerjoin(Order, (Order.customer_id == Customer.id) & (~Order.status.in_(["cancelled"])))
        .outerjoin(OrderItem, OrderItem.order_id == Order.id)
        .group_by(Customer.country)
        .order_by(func.count(func.distinct(Customer.id)).desc())
    ).all()

    return [
        CountryStat(
            country=r.country,
            customer_count=r.customer_count,
            revenue=round(float(r.revenue or 0), 2),
        )
        for r in rows
    ]


@router.get("/new-vs-returning", response_model=List[NewVsReturningPoint])
def get_new_vs_returning(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    # Subquery: first order month per customer
    first_order_subq = (
        select(
            Order.customer_id,
            func.min(Order.created_at).label("first_order"),
        )
        .group_by(Order.customer_id)
        .subquery()
    )

    # Last 6 months cutoff
    now = datetime.utcnow()
    cutoff = datetime(
        now.year - (1 if now.month <= 6 else 0),
        (now.month - 6) % 12 or 12,
        1,
    )

    rows = db.execute(
        select(
            func.strftime("%Y-%m", Order.created_at).label("month"),
            func.sum(
                case(
                    (
                        func.strftime("%Y-%m", Order.created_at)
                        == func.strftime("%Y-%m", first_order_subq.c.first_order),
                        1,
                    ),
                    else_=0,
                )
            ).label("new_customers"),
            func.sum(
                case(
                    (
                        func.strftime("%Y-%m", Order.created_at)
                        != func.strftime("%Y-%m", first_order_subq.c.first_order),
                        1,
                    ),
                    else_=0,
                )
            ).label("returning_customers"),
        )
        .select_from(Order)
        .join(first_order_subq, first_order_subq.c.customer_id == Order.customer_id)
        .where(Order.created_at >= cutoff)
        .group_by(func.strftime("%Y-%m", Order.created_at))
        .order_by(func.strftime("%Y-%m", Order.created_at))
    ).all()

    return [
        NewVsReturningPoint(
            month=r.month,
            new_customers=int(r.new_customers or 0),
            returning_customers=int(r.returning_customers or 0),
        )
        for r in rows
    ]
