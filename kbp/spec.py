from pydantic import UUID4, BaseModel


class TaskSpec(BaseModel):
    name: str


class TaskUpdateSpec(BaseModel):
    id: UUID4
