from datetime import datetime

from fastapi import FastAPI, Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories import UserRepository, SessionRepository


class AuthMiddleware:
    def __init__(self, app: FastAPI):
        self.app = app

    async def __call__(self, request: Request, call_next):
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication credentials were not provided"
            )

        session: AsyncSession = request.state.session
        session_repo = SessionRepository(session)
        db_session = await session_repo.get_by_token(token)

        if db_session is None or db_session.expire_at < datetime.now():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

        user_repo = UserRepository(session)
        user = await user_repo.get(db_session.user_id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        request.state.current_user = user
        response = await call_next(request)
        return response
