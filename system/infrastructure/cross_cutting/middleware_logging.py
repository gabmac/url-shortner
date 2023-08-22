import logging
from datetime import datetime
from typing import Any, Awaitable, Callable, Dict, Optional, Type, Union

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, DispatchFunction
from starlette.types import ASGIApp

from system.infrastructure.adapters.elastic.elastic_logger import ElasticsearchLogger
from system.infrastructure.enums.environment_enum import Environments
from system.infrastructure.settings.config import Config


class RequestContextLogMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        dispatch: DispatchFunction | None = None,
        elastic: Type[ElasticsearchLogger] = ElasticsearchLogger,
    ) -> None:
        super().__init__(app, dispatch)
        self.elastic = None
        if Config.ELASTIC.ACTIVE:
            self.elastic = elastic(
                host=Config.ELASTIC.HOST,
                port=Config.ELASTIC.PORT,
                service_name=Config.ELASTIC.INDEX,
                simulate=True
                if Config.ENVIRONMENT == Environments.LOCAL.value
                else False,
            )

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Any]],
    ) -> Response:
        """_summary_
        Args:
            request (Request)
            call_next (_type_)
        Returns:
            Response
        """
        await self.set_body(request, await request.body())
        request_body = await self.get_body(request)

        response = await call_next(request)

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        response_code = response.status_code
        response_headers = dict(response.headers)
        response_content = response_body.decode()

        if (
            "content-type" in request.headers
            and "multipart/form-data" in request.headers["content-type"]
        ):
            body = ""
        else:
            body = str(request_body.decode())

        document = {
            "@timestamp": datetime.utcnow().isoformat(),
            "method": str(request.method),
            "url": str(request.url),
            "headers": str(dict(request.headers)),
            "body": body,  # type: ignore
            "path-params": str(dict(request.path_params)),
            "query-params": str(dict(request.query_params)),
            "cookies": str(request.cookies),
            "response-code": str(response_code),
            "response-headers": str(response_headers),
            "response-content": str(response_content),
        }

        if self.elastic is not None:
            document["@timestamp"] = datetime.utcnow().isoformat()
            self.elastic.create_document(document_dict=document)

        logger = logging.getLogger(Config.APPLICATION_NAME)
        logger.info("Incoming Request", extra=document)

        return Response(
            content=response_body,  # type: ignore
            status_code=response_code,
            headers=dict(response_headers),
            media_type=response.media_type,  # type: ignore
        )

    async def set_body(self, request: Request, body: bytes) -> None:
        """Set body from RequestArgs"""

        async def receive() -> Optional[Dict[str, Union[bytes, str]]]:
            if self.elastic is not None:
                await self.elastic.set_body(request=request, body=body)
                return None
            else:
                return {"type": "http.request", "body": body}

        request._receive = receive  # type: ignore

    async def get_body(self, request: Request) -> bytes:
        """Get body from request"""
        if self.elastic is not None:
            return await self.elastic.get_body(request=request)

        body = await request.body()
        await self.set_body(request, body)
        return body
