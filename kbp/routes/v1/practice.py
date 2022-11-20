from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import UUID4  # pylint: disable=no-name-in-module

from kbp.boundaries import FileBoundary, TaskBoubndary
from kbp.spec import TaskSpec


router = APIRouter(
    prefix="/practice",
    tags=["practice"],
)


@router.get(
    "/file/{file_id}",
    responses={200: {}, 404: {"model": str, "description": "The item was not found"}},
    response_class=StreamingResponse,
)
async def get_file(
    file_id: UUID4,
    file: FileBoundary = Depends(FileBoundary),
):
    if file_data := await file.get_file(file_id):
        return StreamingResponse(file_data)
    else:
        return Response(f'File: "{file_id}" not found', status_code=404)


@router.post("/file/{task_id}", status_code=201, response_model=UUID4)
async def add_file(
    task_id: UUID4,
    file_data: UploadFile,
    file: FileBoundary = Depends(FileBoundary),
):
    return await file.add_file(task_id, file_data)


@router.get("/task/{task_id}", response_model=TaskSpec)
async def get_task(
    task_id: UUID4,
    task: TaskBoubndary = Depends(TaskBoubndary),
):
    if task_data := await task.get_task(task_id):
        return task_data
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/task", status_code=201)
async def create_task(
    task_data: TaskSpec,
    task: TaskBoubndary = Depends(TaskBoubndary),
):
    task_id = await task.create_task(task_data)
    return {"task_id": task_id}
