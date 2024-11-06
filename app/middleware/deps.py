from fastapi import Request

from libs.database import get_session
from libs.elastic.client import get_es_client


async def add_dependencies(request: Request, call_next):
    session_gen = get_session()
    client_gen = get_es_client()

    try:
        request.state.db = await anext(session_gen)
        request.state.elastic = await anext(client_gen)

        response = await call_next(request)
    finally:
        await session_gen.aclose()
        await client_gen.aclose()

    return response
