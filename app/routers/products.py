from typing import List

from fastapi import Request, APIRouter, HTTPException, status

from app.middleware.auth import authorize
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductSearchRequest
from libs.database.models import Product, ProductState
from libs.database.repositories import ProductRepository

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


def get_product_repository(request: Request) -> ProductRepository:
    return ProductRepository(request.state.db, request.state.elastic)


@router.get("/", response_model=List[ProductResponse])
async def get_products(request: Request, product_search: ProductSearchRequest):
    """Получить список всех продуктов."""
    product_repo = get_product_repository(request)
    products = await product_repo.search_products(
        query=product_search.query,
        filters=product_search.filters,
        cursor=product_search.cursor,
        limit=product_search.limit,
        sort=product_search.sort
    )

    return products


@router.post("/", response_model=ProductResponse)
@authorize()
async def create_product(request: Request, product_data: ProductCreate):
    """Создать новый продукт."""
    product_repo = get_product_repository(request)
    new_product = Product(
        title=product_data.title,
        description=product_data.description,
        price=product_data.price
    )

    new_product.user_id = request.state.current_user.id

    await product_repo.add(new_product)
    return new_product


@router.put("/{product_id}", response_model=ProductResponse)
@authorize()
async def update_product(request: Request, product_id: int, product_data: ProductUpdate):
    """Обновить информацию о продукте."""
    product_repo = get_product_repository(request)
    product = await product_repo.get(product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.user_id != request.state.current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    for field, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    await product_repo.update(product_id, product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
@authorize()
async def delete_product(request: Request, product_id: int):
    """Удалить продукт."""
    product_repo = get_product_repository(request)
    product = await product_repo.get(product_id)

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    if product.user_id != request.state.current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    await product_repo.delete(product_id)
    return {"message": "Product deleted successfully"}
