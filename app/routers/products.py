from typing import List

from fastapi import APIRouter, HTTPException, status

from app.database.engine import SessionDep
from app.database.models.product import Product, ProductState
from app.database.repositories import ProductRepository
from app.middleware.auth import AuthMiddlewareDep
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.get("/", response_model=List[ProductResponse])
async def get_all_products(db: SessionDep):
    """Получить список всех продуктов."""
    product_repo = ProductRepository(db)
    products = await product_repo.get_all()
    return products


@router.post("/", response_model=ProductResponse)
async def create_product(product_data: ProductCreate, db: SessionDep, user: AuthMiddlewareDep):
    product_repo = ProductRepository(db)
    new_product = Product(
        title=product_data.title,
        body=product_data.body,
        price=product_data.price,
        status=ProductState.ACTIVE
    )

    await product_repo.add(new_product)
    return new_product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_data: ProductUpdate, db: SessionDep, user: AuthMiddlewareDep):
    product_repo = ProductRepository(db)
    product = await product_repo.get(product_id)

    if product.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    for field, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    await product_repo.update(product_id, product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, db: SessionDep, user: AuthMiddlewareDep):
    product_repo = ProductRepository(db)
    product = await product_repo.get(product_id)

    if product.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")

    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    await product_repo.delete(product_id)
    return {"message": "Product deleted successfully"}
