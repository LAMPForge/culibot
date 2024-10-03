from urllib.parse import urlencode

from culi.config import settings
from culi.exceptions import CuliRedirectionError, CuliRequestValidationError, CuliError
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.encoders import jsonable_encoder


async def culi_redirection_exception_handler(
    request: Request, exc: CuliRedirectionError
) -> RedirectResponse:
    error_url_params = urlencode(
        {
            "message": exc.message,
            "return_to": exc.return_to or settings.FRONTEND_DEFAULT_RETURN_PATH,
        }
    )
    error_url = f"{settings.generate_frontend_url('/error')}?{error_url_params}"
    return RedirectResponse(error_url, 303)


async def culi_exception_handler(request: Request, exc: CuliError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": type(exc).__name__, "detail": exc.message},
        headers=exc.headers,
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError | CuliRequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"error": type(exc).__name__, "detail": jsonable_encoder(exc.errors())},
    )


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        CuliRedirectionError,
        culi_redirection_exception_handler,  # type: ignore
    )
    app.add_exception_handler(
        RequestValidationError,
        request_validation_exception_handler,  # type: ignore
    )
    app.add_exception_handler(
        CuliRequestValidationError,
        request_validation_exception_handler,  # type: ignore
    )
    app.add_exception_handler(CuliError, culi_exception_handler)  # type: ignore
