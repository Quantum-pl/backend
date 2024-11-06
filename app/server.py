from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.middleware.deps import add_dependencies
from app.routers import users, auth, orders, products
from libs.database import init_db, get_session
from libs.elastic.client import es_client, sync_elasticsearch


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    async for session in get_session():
        await sync_elasticsearch(session)

    yield
    await es_client.close()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(BaseHTTPMiddleware, dispatch=add_dependencies)

    app.include_router(users.router)
    app.include_router(auth.router)
    app.include_router(orders.router)
    app.include_router(products.router)

    origins = [
        "http://localhost",
        "http://localhost:8080",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
