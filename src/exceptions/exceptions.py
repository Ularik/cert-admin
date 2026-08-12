class NoResultException(Exception):
    detail = "Ошибка"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ObjectNotFoundException(NoResultException):
    detail = "Объект не найден"


class DepartmentNotFoundException(ObjectNotFoundException):
    detail = "Отдел не найден"


class UniqueObjIsExistException(Exception):
    detail = 'Такой объект уже существует'