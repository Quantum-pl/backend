from typing import List

from fastapi import Request, APIRouter, HTTPException, status

from app.middleware.auth import authorize
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from libs.database import SessionDep
from libs.database.models import Order, OrderState
from libs.database.repositories import OrderRepository

router = APIRouter(
    prefix="/orders",
    tags=["orders"]
)


@router.get("/", response_model=List[OrderResponse])
@authorize()
async def get_user_orders(request: Request):
    """Получить список всех заказов пользователя."""
    product_repo = OrderRepository(request.state.db)
    products = await product_repo.get_user_orders(request.state.current_user.id)
    return products


@router.post("/", response_model=OrderResponse)
@authorize()
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
@authorize()
async def update_order(request: Request, order_id: int, data: OrderUpdate):
    order_repo = OrderRepository(request.state.db)
    order = await order_repo.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.user_id != request.state.current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(order, field, value)

    await order_repo.update(order_id, order)
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
@authorize()
async def delete_order(request: Request, order_id: int):
    order_repo = OrderRepository(request.state.db)
    order = await order_repo.get(order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    if order.user_id != request.state.current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    await order_repo.delete(order)
    return {"message": "Order deleted successfully"}
