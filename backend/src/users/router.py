from fastapi import APIRouter, status

from src.users.dependencies import CurrentAdminDep, CurrentUserDep, UserServiceDep
from src.users.schemas import LoginRequest, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login")
async def login(data: LoginRequest, service: UserServiceDep):
    return await service.login(data)


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUserDep):
    return current_user


@router.patch("/me", response_model=UserRead)
async def update_me(data: UserUpdate, current_user: CurrentUserDep, service: UserServiceDep):
    return await service.update_user(str(current_user.id), data)


@router.get("", response_model=list[UserRead])
async def list_users(service: UserServiceDep, _user: CurrentUserDep):
    return await service.list_users()


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, service: UserServiceDep, _admin: CurrentAdminDep):
    return await service.create_user(data)


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: str, data: UserUpdate, service: UserServiceDep, _admin: CurrentAdminDep
):
    return await service.update_user(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, service: UserServiceDep, _admin: CurrentAdminDep):
    await service.delete_user(user_id)
