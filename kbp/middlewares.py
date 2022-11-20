from typing import Callable
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware

from kbp.config import config


def add_middlewares(app: Starlette, *middlewares: Callable):
    for middleware in middlewares:
        app.add_middleware(BaseHTTPMiddleware, dispatch=middleware)


async def database_connection(request: Request, callback: Callable):
    session = AsyncSession(config.pg.get_engine())
    try:
        request.state.db_session = session
        return await callback(request)
    finally:
        session.close()


async def fs_connection(request: Request, callback: Callable):
    async with config.fs.get_resource() as s3:
        request.state.s3resource = s3
        response = await callback(request)
    return response
