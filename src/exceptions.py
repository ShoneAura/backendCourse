class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *argsб, **kwargs):
        super().__init__(self.detail, *argsб, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Нет свободных номеров"


class ObjectIsAlreadyExistsException(NabronirovalException):
    detail = "Объект уже существует"

class DatesAreIncorrectException(NabronirovalException):
    detail = "Некорректные даты"