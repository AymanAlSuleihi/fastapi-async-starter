from sqlalchemy import select

from src.auth.exceptions import InvalidCredentials
from src.auth.schemas import TokenResponse
from src.auth.utils import create_access_token, hash_password, verify_password
from src.db.engine import DbDep
from src.users.exceptions import UserAlreadyExists, UserNotFound
from src.users.models import User
from src.users.schemas import LoginRequest, UserCreate, UserUpdate


class UserService:
    def __init__(self, db: DbDep):
        self.db = db

    async def login(self, data: LoginRequest) -> TokenResponse:
        admin = await self.db.scalar(select(User).where(User.email == data.email))
        if not admin or not verify_password(data.password, admin.hashed_password):
            raise InvalidCredentials()
        token_data = {"sub": str(admin.id)}
        return TokenResponse(
            access_token=create_access_token(token_data),
            refresh_token="",
            token_type="bearer",
        )

    async def list_users(self) -> list[User]:
        result = await self.db.execute(select(User).order_by(User.created_at.desc()))
        return list(result.scalars().all())

    async def create_user(self, data: UserCreate) -> User:
        existing = await self.db.scalar(select(User).where(User.email == data.email))
        if existing:
            raise UserAlreadyExists()
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            first_name=data.first_name,
            last_name=data.last_name,
            is_admin=data.is_admin,
            is_active=data.is_active,
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_user(self, user_id: str, data: UserUpdate) -> User:
        user = await self.db.scalar(select(User).where(User.id == user_id))
        if not user:
            raise UserNotFound(user_id)
        if data.first_name is not None:
            user.first_name = data.first_name
        if data.last_name is not None:
            user.last_name = data.last_name
        if data.email is not None:
            user.email = data.email
        if data.password is not None:
            user.hashed_password = hash_password(data.password)
        if data.is_admin is not None:
            user.is_admin = data.is_admin
        if data.is_active is not None:
            user.is_active = data.is_active
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: str) -> None:
        user = await self.db.scalar(select(User).where(User.id == user_id))
        if not user:
            raise UserNotFound(user_id)
        await self.db.delete(user)
        await self.db.commit()
