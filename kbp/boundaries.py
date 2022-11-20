from pathlib import Path
from typing import Iterator, Optional
from fastapi import Request, UploadFile
from pydantic import UUID4
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from kbp.config import config
from kbp.models import FileModel, TaskModel
from kbp.spec import TaskSpec


class TaskBoubndary:
    """SMTHUSEFUL"""

    def __init__(self, request: Request) -> None:
        self._db_session: AsyncSession = request.state.db_session

    async def create_task(self, task: TaskSpec) -> UUID4:
        async with self._db_session.begin():
            q = insert(TaskModel).values(name=task.name).returning(TaskModel.id)
            result = await self._db_session.execute(q)
            return result.first()["id"]

    async def get_task(self, task_id: UUID4) -> Optional[TaskSpec]:
        async with self._db_session.begin():
            result = await self._db_session.execute(
                select(TaskModel).where(TaskModel.id == task_id)
            )
            return result.first()


class FileBoundary:
    """SMTHUSEFUL"""

    def __init__(self, request: Request) -> None:
        self._db_session: AsyncSession = request.state.db_session
        self._s3resource = request.state.s3resource

    async def add_file(
        self, task_id: UUID4, file: UploadFile, subpath: str = ""
    ) -> None:
        p = Path(f"task={task_id}")
        file_path = str(p / subpath / file.filename)
        async with self._db_session.begin():
            row = await self._db_session.execute(
                insert(FileModel)
                .values(
                    path=file_path,
                    task_id=task_id,
                )
                .returning(FileModel.id)
            )
            bucket = await self._s3resource.Bucket(config.fs.buckets.mentors)
            await bucket.put_object(
                Key=file_path,
                Body=await file.read(),
            )
            return row.first()["id"]

    async def get_file(self, file_id: UUID4) -> Optional[Iterator[bytes]]:
        async with self._db_session.begin():
            q = select(FileModel.path).where(FileModel.id == file_id)
            r = await self._db_session.execute(q)
            if file_row := r.first():
                bucket = await self._s3resource.Bucket(config.fs.buckets.mentors)
                file_object = await bucket.Object(file_row["path"])
                data = await file_object.get()
                return data["Body"].iter_chunks()
