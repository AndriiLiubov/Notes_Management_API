from datetime import datetime
from pydantic import BaseModel, Field


class NoteModel(BaseModel):
    title: str = Field(max_length=50)
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class NoteResponse(NoteModel):
    id: int

    class Config:
        orm_mode = True


class NoteVersionResponse(BaseModel):
    id: int
    note_id: int
    title: str = Field(max_length=50)
    content: str
    created_at: datetime

    class Config:
        orm_mode = True
