# pylint: disable=missing-class-docstring

import aioboto3
import boto3
from functools import wraps
from pydantic import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import QueuePool


def singleton(func):
    data = None

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal data
        if data is None:
            data = func(*args, **kwargs)
        return data

    return wrapper


class PostgresSettings(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    db: str = "kbpdb"
    user: str
    password: str

    class Config:
        # pylint: disable=too-few-public-methods
        env_prefix = "postgres_"

    @singleton
    def get_engine(self) -> AsyncEngine:
        return create_async_engine(
            self.get_uri(),
            poolclass=QueuePool,
            pool_timeout=120,  # seconds
            pool_size=5,
        )

    def get_uri(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class FSBuckets(BaseSettings):
    class Config:
        # pylint: disable=too-few-public-methods
        env_prefix = "fs_bucket_"

    mentors: str


class FSSettings(BaseSettings):
    class Config:
        # pylint: disable=too-few-public-methods
        env_prefix = "fs_"

    host: str
    port: int
    access_key: str
    secret_key: str
    signature_version: str = "s3v4"

    buckets: FSBuckets = FSBuckets()

    def get_resource(self):
        session = aioboto3.Session()
        return session.resource(
            's3',
            endpoint_url=f'http://{self.host}:{self.port}',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            config=boto3.session.Config(signature_version=self.signature_version),
            verify=False,
        )


class Config(BaseSettings):
    pg: PostgresSettings = PostgresSettings()
    fs: FSSettings = FSSettings()


config = Config()
