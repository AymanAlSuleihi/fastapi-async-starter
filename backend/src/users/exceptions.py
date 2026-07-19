from src.core.exceptions import ConflictException, NotFoundException


class UserNotFound(NotFoundException):
    def __init__(self, user_id: str | None = None):
        detail = f"User with id {user_id} not found" if user_id else "User not found"
        super().__init__(detail=detail, code="USER_NOT_FOUND")


class UserAlreadyExists(ConflictException):
    def __init__(self):
        super().__init__(detail="A user with this email already exists", code="USER_ALREADY_EXISTS")
