from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.order import OrderStatus


class OrderBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    status: OrderStatus = OrderStatus.pending


class OrderCreate(OrderBase):
    pass


class OrderUpdate(OrderBase):
    pass


class OrderRead(OrderBase):
    id: int
    total_amount: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
