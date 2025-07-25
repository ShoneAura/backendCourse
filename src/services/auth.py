from datetime import datetime, timezone, timedelta
from fastapi import Response

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from src.config import settings
from src.exceptions import UserIsAlreadyExistsException, ObjectIsAlreadyExistsException, UserNotFoundException, \
    UserWrongPasswordException
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.base import BaseService


class AuthService(BaseService):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(
            to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def hash_password(self, password):
        return self.pwd_context.hash(password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")

    async def register_user(self, data: UserRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectIsAlreadyExistsException as ex:
            raise UserIsAlreadyExistsException from ex

    async def login_user(self, data: UserRequestAdd, response: Response):
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise UserNotFoundException
        if not self.verify_password(
                data.password, hashed_password=user.hashed_password
        ):
            raise UserWrongPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        response.set_cookie(key="access_token", value=access_token)
        return {"access_token": access_token}

    async def get_me(
            self,
            user_id: int,
    ):
        try:
            return await self.db.users.get_one(id=user_id)
        except UserNotFoundException as ex:
            raise UserNotFoundException from ex

    async def logout_user(self, response: Response):
        response.delete_cookie(key="access_token")
