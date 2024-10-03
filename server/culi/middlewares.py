from starlette.types import ASGIApp, Message, Receive, Scope, Send
import re
import functools
from starlette.datastructures import MutableHeaders


class PathRewriteMiddleware:
    def __init__(
        self, app: ASGIApp, pattern: str | re.Pattern[str], replacement: str
    ) -> None:
        self.app = app
        self.pattern = pattern
        self.replacement = replacement

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        scope["path"], replacements = re.subn(
            self.pattern, self.replacement, scope["path"]
        )

        send = functools.partial(self.send, send=send, replacements=replacements)
        await self.app(scope, receive, send)

    @staticmethod
    async def send(message: Message, send: Send, replacements: int) -> None:
        if message["type"] != "http.response.start":
            await send(message)
            return

        message.setdefault("headers", [])
        headers = MutableHeaders(scope=message)
        if replacements > 0:
            headers["X-Culi-Deprecation-Notice"] = (
                "The API root has moved from /api/v1 to /v1. "
                "Please update your integration."
            )

        await send(message)
