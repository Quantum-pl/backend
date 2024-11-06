from datetime import datetime
from functools import wraps
from typing import List, Optional, Callable, Annotated

from fastapi import Request, HTTPException, status
from fastapi.params import Depends

from app.utils.auth import hash_token
from libs.database import SessionDep
from libs.database.models import User, UserFlag
from libs.database.repositories import SessionRepository


def authorize(flags: Optional[List[UserFlag]] = None):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, request: Request, **kwargs):
            user = await get_authenticated_user(request, request.state.db)
            if flags and not any(user.flags & flag.value for flag in flags):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

            request.state.current_user = user
            return await func(*args, request=request, **kwargs)

        return wrapper

    return decorator


async def get_authenticated_user(
        request: Request,
        session: SessionDep
) -> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided"
        )

    session_repo = SessionRepository(session)
    db_session = await session_repo.get_by_access_token(hash_token(token), relations=["user"])

    if db_session is None or db_session.expire_at < datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = db_session.user
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


AuthUserDep = Annotated[User, Depends(get_authenticated_user)]
