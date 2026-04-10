from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional

class UserRole(Enum):
    AGENCY = "AGENCY"
    CLIENT = "CLIENT"

class PostStatus(Enum):
    PENDING_UPLOAD = "PENDING_UPLOAD"
    CRIADO = "CRIADO"
    AGUARDANDO_APROVACAO = "AGUARDANDO_APROVACAO"
    APROVADO = "APROVADO"
    REJEITADO = "REJEITADO"

class Coordinate(BaseModel):
    x: float
    y: float

class User(BaseModel):
    id: UUID
    name: str
    email: str
    password_hash: str
    role: UserRole

class CommentEntity(BaseModel):
    id: UUID = Field(..., description="ID Único Universal do Comentário")
    post_id: UUID = Field(..., description="Vínculo com a mídia original")
    user_id: UUID = Field(..., description="Autor do comentário")
    content: str = Field(..., description="Texto do feedback visual", example="Ajustar brilho no frame 02")
    coord_x: float = Field(..., description="Posição X (0-100) no Canvas", example=45.5)
    coord_y: float = Field(..., description="Posição Y (0-100) no Canvas", example=78.2)
    created_at: Optional[datetime] = Field(None, description="Data de criação no fuso de SP")

class PostEntity(BaseModel):
    id: UUID = Field(..., description="ID Identificador do Post")
    calendar_id: UUID = Field(..., description="Vínculo com o calendário da campanha")
    media_url: str = Field(..., description="Link final S3 da mídia", example="https://s3.aws.com/video.mp4")
    status: PostStatus = Field(PostStatus.CRIADO, description="Estado atual no Kanban B2B")
    comments: List[CommentEntity] = Field([], description="Lista de Pins/ feedbacks visuais")
    created_at: Optional[datetime] = Field(None, description="Data de entrada no sistema")

class Post(PostEntity):
    pass

class Comment(CommentEntity):
    @property
    def coord(self):
        return Coordinate(x=self.coord_x, y=self.coord_y)
