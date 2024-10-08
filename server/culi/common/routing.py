import functools
from typing import Any, ParamSpec, TypeVar

from fastapi.routing import APIRoute
from collections.abc import Callable
from fastapi import APIRouter as _APIRouter
from sqlalchemy.ext.asyncio import AsyncSession


class AutoCommitAPIRoute(APIRoute):
    """
    A subclass of `APIRoute` that automatically
    commits the session after the endpoint is called.

    It allows to directly return ORM objects from the endpoint
    without having to call `session.commit()` before returning.
    """
    def __init__(self, path: str, endpoint: Callable[..., Any], **kwargs: Any) -> None:
        endpoint = self.wrap_endpoint(endpoint)
        super().__init__(path, endpoint, **kwargs)

    @staticmethod
    def wrap_endpoint(endpoint: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(endpoint)
        async def wrapped_endpoint(*args: Any, **kwargs: Any) -> Any:
            session: AsyncSession | None = None
            for arg in (args, *kwargs.values()):
                if isinstance(arg, AsyncSession):
                    session = arg
                    break

            response = await endpoint(*args, **kwargs)

            if session is not None:
                await session.commit()

            return response

        return wrapped_endpoint


_P = ParamSpec("_P")
_T = TypeVar("_T")


def _inherit_signature_from(
    _to: Callable[_P, _T],
) -> Callable[[Callable[..., _T]], Callable[_P, _T]]:
    return lambda x: x  # pyright: ignore

def get_api_router_class(route_class: type[APIRoute]) -> type[_APIRouter]:
    """
    Returns a subclass of `APIRouter` that uses the given `route_class`.
    """

    class _CustomAPIRouter(_APIRouter):
        @_inherit_signature_from(_APIRouter.__init__)
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            kwargs["route_class"] = route_class
            super().__init__(*args, **kwargs)

    return _CustomAPIRouter

__all__ = ["get_api_router_class", "AutoCommitAPIRoute"]
