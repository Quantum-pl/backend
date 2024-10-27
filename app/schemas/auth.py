from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    """Схема для регистрации нового пользователя."""
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class LoginRequest(BaseModel):
    """Схема для запроса на вход в систему."""
    email: str
    password: str


class LoginResponse(BaseModel):
    """Схема ответа при успешной аутентификации."""
    token: str
    refresh_token: str
