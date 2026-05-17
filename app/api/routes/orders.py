from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_admin_user, get_current_user, get_db
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate


router = APIRouter()


def calculate_total_amount(product: Product, quantity: int) -> Decimal:
    return product.price * quantity


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
) -> Order:
    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if product.stock < payload.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock")

    order = Order(
        **payload.model_dump(),
        total_amount=calculate_total_amount(product, payload.quantity),
    )
    db.add(order)
    product.stock -= payload.quantity
    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=list[OrderRead])
def list_orders(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[Order]:
    return db.query(Order).order_by(Order.id.desc()).all()


@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderRead)
def update_order(
    order_id: int,
    payload: OrderUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
) -> Order:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    user = db.query(User).filter(User.id == payload.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.id == order.product_id:
        available_stock = product.stock + order.quantity
    else:
        available_stock = product.stock

    if available_stock < payload.quantity:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough stock")

    previous_product = db.query(Product).filter(Product.id == order.product_id).first()
    if previous_product:
        previous_product.stock += order.quantity
    product.stock -= payload.quantity

    for field, value in payload.model_dump().items():
        setattr(order, field, value)
    order.total_amount = calculate_total_amount(product, payload.quantity)

    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(get_admin_user),
) -> Response:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    product = db.query(Product).filter(Product.id == order.product_id).first()
    if product:
        product.stock += order.quantity

    db.delete(order)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
