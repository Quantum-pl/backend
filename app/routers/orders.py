# routes/orders.py
from typing import List

from fastapi import APIRouter, HTTPException, status

from app.database.engine import SessionDep
from app.database.models.order import Order, OrderState
from app.database.repositories.order import OrderRepository
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)

@router.get("/", response_model=List[OrderResponse])
async def get_all_products(db: SessionDep):
    """Получить список всех продуктов."""
    product_repo = OrderRepository(db)
    products = await product_repo.get_all()
    return products


@router.post("/", response_model=OrderResponse)
async def create_order(order_data: OrderCreate, db: SessionDep):
    order_repo = OrderRepository(db)
    new_order = Order(
        user_id=order_data.user_id,
        status=OrderState.CREATED
    )
    new_order.products = order_data.products
    await order_repo.add(new_order)
    return new_order


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(order_id: int, data: OrderUpdate, db: SessionDep):
    order_repo = OrderRepository(db)
    order = await order_repo.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(order, field, value)

    await order_repo.update(order_id, order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, db: SessionDep):
    order_repo = OrderRepository(db)
    order = await order_repo.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    await order_repo.delete(order)
    return {"message": "Order deleted successfully"}
