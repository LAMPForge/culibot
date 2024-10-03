from culi.common.routing import get_api_router_class, AutoCommitAPIRoute


class APIRoute(
    AutoCommitAPIRoute
):
    pass


APIRouter = get_api_router_class(APIRoute)


__all__ = ["APIRouter", "APIRoute"]
