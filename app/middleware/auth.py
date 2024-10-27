from datetime import datetime
from typing import Annotated

from fastapi import Request, HTTPException, status, Depends

from app.database.engine import SessionDep
from app.database.models import User
from app.database.repositories import SessionRepository
from app.utils.auth import hash_token


async def get_authorization(request: Request, session: SessionDep):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided"
        )

    session_repo = SessionRepository(session)
    db_session = await session_repo.get_by_token(hash_token(token), relations=["user"])

    if db_session is None or db_session.expire_at < datetime.now():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    user = db_session.user

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    request.state.current_user = user
    return user


AuthMiddlewareDep = Annotated[User, Depends(get_authorization)]
