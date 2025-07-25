from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *argsб, **kwargs):
        super().__init__(self.detail, *argsб, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"


class UserNotFoundException(ObjectNotFoundException):
    detail = "Пользователь не найден"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Нет свободных номеров"


class ObjectIsAlreadyExistsException(NabronirovalException):
    detail = "Объект уже существует"

class UserIsAlreadyExistsException(ObjectIsAlreadyExistsException):
    detail = "Пользователь уже существует"

class DatesAreIncorrectException(NabronirovalException):
    detail = "Некорректные даты"

class UserWrongPasswordException(NabronirovalException):
    detail = "Не верный пароль"

def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть позже даты выезда")

class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"

class UserNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой не найден"

class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Нет свободных номеров для бронирования"

class UserIsAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Такой пользователь уже существует"

class UserWrongPasswordHTTPException(NabronirovalHTTPException):
    status_code = 401
    detail = "Не верный пароль"