from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func, case, select
from sqlalchemy.orm import Session

from database import get_db
from models import Order, OrderItem, Product
from routers.auth import get_current_user
from schemas import TopProduct, CategoryStat, ProductReturnRate

router = APIRouter()


@router.get("/top", response_model=List[TopProduct])
def get_top_products(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    revenue_expr = func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), 0.0)

    rows = db.execute(
        select(
            Product.id,
            Product.name,
            Product.category,
            revenue_expr.label("revenue"),
            func.coalesce(func.sum(OrderItem.quantity), 0).label("units_sold"),
        )
        .select_from(Product)
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
        .where(~Order.status.in_(["cancelled"]))
        .group_by(Product.id, Product.name, Product.category)
        .order_by(revenue_expr.desc())
        .limit(10)
    ).all()

    return [
        TopProduct(
            product_id=r.id,
            name=r.name,
            category=r.category,
            revenue=round(float(r.revenue), 2),
            units_sold=int(r.units_sold),
        )
        for r in rows
    ]


@router.get("/by-category", response_model=List[CategoryStat])
def get_products_by_category(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    revenue_expr = func.coalesce(func.sum(OrderItem.quantity * OrderItem.unit_price), 0.0)

    rows = db.execute(
        select(
            Product.category,
            revenue_expr.label("revenue"),
            func.count(func.distinct(Order.id)).label("orders"),
        )
        .select_from(Product)
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
        .where(~Order.status.in_(["cancelled"]))
        .group_by(Product.category)
        .order_by(revenue_expr.desc())
    ).all()

    return [
        CategoryStat(category=r.category, revenue=round(float(r.revenue), 2), orders=r.orders)
        for r in rows
    ]


@router.get("/return-rate", response_model=List[ProductReturnRate])
def get_return_rate(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_user),
):
    returned_expr = func.sum(case((Order.status == "returned", 1), else_=0))
    total_expr = func.count(Order.id)
    rate_expr = returned_expr * 1.0 / total_expr

    rows = db.execute(
        select(
            Product.id,
            Product.name,
            Product.category,
            total_expr.label("total_orders"),
            returned_expr.label("returned_orders"),
        )
        .select_from(Product)
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
        .group_by(Product.id, Product.name, Product.category)
        .having(total_expr > 0)
        .order_by(rate_expr.desc())
        .limit(10)
    ).all()

    return [
        ProductReturnRate(
            product_id=r.id,
            name=r.name,
            category=r.category,
            total_orders=r.total_orders,
            returned_orders=int(r.returned_orders or 0),
            return_rate=round(float(r.returned_orders or 0) / float(r.total_orders), 4),
        )
        for r in rows
    ]
