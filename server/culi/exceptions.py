from typing import Literal, TypedDict, LiteralString, Any
from pydantic import BaseModel, create_model
from pydantic_core import ErrorDetails, InitErrorDetails, PydanticCustomError
from pydantic_core import ValidationError as PydanticValidationError


class CuliError(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.headers = headers or {}

    @classmethod
    def schema(cls) -> type[BaseModel]:
        type_literal = Literal[cls.__name__] # type: ignore

        return create_model(cls.__name__, type=(type_literal, ...), detail=(str, ...))


class CuliRedirectionError(CuliError):
    def __init__(
        self, message: str, status_code: int = 400, return_to: str | None = None
    ) -> None:
        self.return_to = return_to
        super().__init__(message, status_code)


class BadRequest(CuliError):
    def __init__(self, message: str = "Bad request", status_code: int = 400) -> None:
        super().__init__(message, status_code)


class NotPermitted(CuliError):
    def __init__(self, message: str = "Not permitted", status_code: int = 403) -> None:
        super().__init__(message, status_code)


class Unauthorized(CuliError):
    def __init__(self, message: str = "Unauthorized", status_code: int = 401) -> None:
        super().__init__(
            message,
            status_code,
            headers={
                "WWW-Authenticate": 'Bearer'
            },
        )


class InternalServerError(CuliError):
    def __init__(
        self, message: str = "Internal Server Error", status_code: int = 500
    ) -> None:
        super().__init__(message, status_code)


class ResourceNotFound(CuliError):
    def __init__(self, message: str = "Not found", status_code: int = 404) -> None:
        super().__init__(message, status_code)


class ResourceUnavailable(CuliError):
    def __init__(self, message: str = "Unavailable", status_code: int = 410) -> None:
        super().__init__(message, status_code)


class ResourceAlreadyExists(CuliError):
    def __init__(self, message: str = "Already exists", status_code: int = 409) -> None:
        super().__init__(message, status_code)


class ValidationError(TypedDict):
    loc: tuple[int | str, ...]
    msg: LiteralString
    type: LiteralString
    input: Any


class CuliRequestValidationError(CuliError):
    def __init__(self, errors: list[ValidationError]) -> None:
        self._errors = errors

    def errors(self) -> list[ErrorDetails]:
        pydantic_errors: list[InitErrorDetails] = []
        for error in self._errors:
            pydantic_errors.append(
                {
                    "type": PydanticCustomError(error["type"], error["msg"]),
                    "loc": error["loc"],
                    "input": error["input"],
                }
            )
        pydantic_error = PydanticValidationError.from_exception_data(
            self.__class__.__name__, pydantic_errors
        )
        return pydantic_error.errors()
