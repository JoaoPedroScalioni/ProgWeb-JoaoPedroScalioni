from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional

class CommentEntity(BaseModel):
    id: UUID
    post_id: UUID
    user_id: UUID
    content: str
    coord_x: float
    coord_y: float

class PostEntity(BaseModel):
    id: UUID
    calendar_id: UUID
    media_url: str
    status: str
    comments: List[CommentEntity] = []
