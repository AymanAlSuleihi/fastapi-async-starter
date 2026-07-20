from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from src.core.config import settings
from src.core.exceptions import ForbiddenException
from src.db.engine import DbDep
from src.users.models import User
from src.users.service import UserService

user_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/users/login", auto_error=False
)


async def get_current_user(
    db: DbDep,
    token: Annotated[str | None, Depends(user_scheme)],
) -> User:
    from src.auth.utils import decode_token

    if not token:
        raise ForbiddenException(detail="Authentication required")

    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise ForbiddenException(detail="Authentication required")

    user = await db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise ForbiddenException(detail="Authentication required")
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_admin(current_user: CurrentUserDep) -> User:
    if not current_user.is_admin:
        raise ForbiddenException(detail="Admin access required")
    return current_user


CurrentAdminDep = Annotated[User, Depends(get_current_admin)]


async def get_user_service(db: DbDep) -> UserService:
    return UserService(db)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
