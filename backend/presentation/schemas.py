from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID
from backend.domain.entities import PostStatus
from typing import Optional, List

# ===============================================
# Kanban Posts Schemas
# ===============================================
class PostCreateRequest(BaseModel):
    calendar_id: UUID = Field(..., description="ID B2B do calendário associado ao Cliente/Agência")
    media_url: str = Field(..., description="Link Pre-signed S3 da mídia blindando a RAM do servidor")

class PostResponse(BaseModel):
    id: UUID = Field(..., description="Identificador universal rígido do Post Kanban")
    calendar_id: UUID
    media_url: str
    status: PostStatus = Field(..., description="Motor de estado restrito RFC 2119")
    
    model_config = ConfigDict(from_attributes=True)

# ===============================================
# Pins Visuais (Comments) Schemas 
# ===============================================
class CommentCreateRequest(BaseModel):
    user_id: UUID = Field(..., description="UUID do Cliente autor do Feedback Visual")
    content: str = Field(..., description="A notação ou ordem corretiva solicitada")
    
    # Regra de Ouro: Coordenadas obrigatoriamente entre 0 e 100 porcento de posicionamento Relativo Front-end.
    coord_x: float = Field(..., ge=0.0, le=100.0, description="Posição Horizontal (X) em Porcentagem %")
    coord_y: float = Field(..., ge=0.0, le=100.0, description="Posição Vertical (Y) em Porcentagem %")

class CommentResponse(BaseModel):
    id: UUID
    post_id: UUID
    user_id: UUID
    content: str
    coord_x: float = Field(..., description="Coordenada X chumbada do clique")
    coord_y: float = Field(..., description="Coordenada Y chumbada do clique")

    model_config = ConfigDict(from_attributes=True)

# ===============================================
# Upload Intent Schemas (AWS S3 Bypass)
# ===============================================
class UploadIntentRequest(BaseModel):
    filename: str = Field(..., description="Nome sujo do arquivo original da máquina do cliente.")
    content_type: str = Field(..., description="Formato binário padrão HTTP Mime (Ex: video/mp4)")
    calendar_id: UUID = Field(..., description="UUID reativo para injetar o 'fantasma' do Post no PostgreSQL.")

class UploadIntentResponse(BaseModel):
    upload_url: str = Field(..., description="URL estritamente efêmera (5 minutos) assinada pelo AWS.")
    file_key: str = Field(..., description="A key purificada UUID v4 que será lida pelo storage no futuro.")

# ===============================================
# Aggregate/Detail Schemas
# ===============================================
class PostDetailResponse(PostResponse):
    """Resposta Agregada puxando os Pins via Eager Loading SQLAlchemy"""
    comments: List[CommentResponse] = Field(default=[], description="Coleção de Pins Visuais vinculados")

class ApprovePostRequest(BaseModel):
    client_id: UUID
