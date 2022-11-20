# pylint: disable=missing-class-docstring,too-few-public-methods

from alembic import command, config
from sqlalchemy import Column, ForeignKey, Text, text, VARCHAR
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine


Base = declarative_base()


def run_upgrade(connection, cfg):
    cfg.attributes['connection'] = connection
    command.upgrade(cfg, 'head')


async def run_async_upgrade(uri: str):
    async_engine = create_async_engine(uri, echo=True)
    async with async_engine.begin() as conn:
        await conn.run_sync(run_upgrade, config.Config('alembic.ini'))


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()')
    )
    name = Column(
        Text, nullable=False
    )


class UserModel(Base):
    __tablename__ = 'users'

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()')
    )


class FileModel(Base):
    __tablename__ = 'files'

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text('gen_random_uuid()')
    )
    path = Column(VARCHAR(length=256), nullable=False)
    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'))
