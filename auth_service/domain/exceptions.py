class InvalidCredentialsError(Exception):
    """Неверные учетные данные."""
    
    def __init__(self, message: str = "Неверно введены логин или пароль"):
        super().__init__(message)


class UserNotFoundError(Exception):
    """Пользователь не найден."""
    
    def __init__(self, message: str = "Пользователь не найден"):
        super().__init__(message)


class InvalidOldPasswordError(Exception):
    """Ошибка старого пароля"""
    def __init__(self, message: str = "Старый пароль введен неверно"):
        super().__init__(message)