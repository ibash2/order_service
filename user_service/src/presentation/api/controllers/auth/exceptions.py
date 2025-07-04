from domain.common.exceptions.base import DomainError


class AuthException(DomainError):
    @property
    def message(self):
        return "Authorization error"


class AuthRequired(AuthException):
    @property
    def message(self):
        return "Authorization is required"


class InvalidToken(AuthException):
    @property
    def message(self):
        return "Invalid token"
