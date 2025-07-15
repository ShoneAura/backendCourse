from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import UserIsAlreadyExistsHTTPException, \
    UserIsAlreadyExistsException, NabronirovalHTTPException, UserNotFoundException, UserNotFoundHTTPException, \
    UserWrongPasswordHTTPException
from src.schemas.users import UserRequestAdd
from src.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация и Аутентификация"],
)


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    try:
        await AuthService(db).register_user(data=data)
    except UserIsAlreadyExistsException:
        raise UserIsAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(db: DBDep, data: UserRequestAdd, response: Response):
    try:
        return await AuthService(db).login_user(data, response)
    except UserNotFoundException:
        raise UserNotFoundHTTPException
    except NabronirovalHTTPException as ex:
        raise UserWrongPasswordHTTPException


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep,
):
    try:
        return await AuthService(db).get_me(user_id)
    except UserNotFoundException:
        raise UserNotFoundHTTPException


@router.post("/logout")
async def logout_user(response: Response):
    await AuthService().logout_user(response)
    return {"status": "OK"}
