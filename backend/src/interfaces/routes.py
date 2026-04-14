from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from src.interfaces.schemas import (
    PostCreateRequest, 
    PostResponse, 
    CommentCreateRequest, 
    CommentResponse,
    PostDetailResponse,
    UploadIntentRequest,
    UploadIntentResponse
)
from src.infrastructure.database import get_db, get_storage
from src.infrastructure.models import PostModel, CommentModel, UserModel
from src.domain.repositories import StorageRepository
from src.domain.entities import PostStatus
from src.interfaces.auth import get_current_user
from src.application.use_cases import GetPostDetailUseCase, AddCommentUseCase
from src.infrastructure.repositories_impl import PostRepositorySQLAlchemy
from src.infrastructure.utils.time_service import TimeService

router = APIRouter(prefix="/posts", tags=["Kanban Posts B2B"])

@router.post("/upload-intent", response_model=UploadIntentResponse, status_code=201)
async def create_upload_intent(
    request: UploadIntentRequest, 
    db: AsyncSession = Depends(get_db),
    storage: StorageRepository = Depends(get_storage)
):
    """
    RFC 2119: Emissão Efêmera da Pre-signed URL para arquitetura Cloud-first.
    A API interceptará a solicitação de intenção de Upload do Canvas, 
    sobrescreverá o nome falho para um UUID v4 B2B e persistirá a casca no DB 
    como 'PENDING_UPLOAD'.
    """
    presigned = storage.generate_upload_url(
        file_name=request.filename, 
        file_type=request.content_type
    )
    
    new_post = PostModel(
        calendar_id=request.calendar_id,
        media_url=presigned["file_key"],
        status=PostStatus.PENDING_UPLOAD,
        created_at=TimeService.get_now()
    )
    db.add(new_post)
    await db.commit()
    
    return UploadIntentResponse(
        upload_url=presigned["upload_url"],
        file_key=presigned["file_key"]
    )

@router.post("", response_model=PostResponse, status_code=201)
async def create_post(
    request: PostCreateRequest, 
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Cadastra uma nova mídia aprovável no pipeline Kanban.
    Chamado após o Front-end confirmar o upload de 500MB via S3.
    """
    new_post = PostModel(
        calendar_id=request.calendar_id,
        media_url=request.media_url,
        created_at=TimeService.get_now()
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

@router.get("/{post_id}", response_model=PostDetailResponse, responses={404: {"description": "Post não localizado"}})
async def get_post(post_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Obtém a mídia delegando ao Caso de Uso (Application Layer) via Repository.
    Erros de domínio (404) são capturados pelo Exception Handler Global.
    """
    repo = PostRepositorySQLAlchemy(db)
    use_case = GetPostDetailUseCase(repo)
    return await use_case.execute(post_id)

@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=201, responses={404: {"description": "Post não localizado"}, 400: {"description": "Coordenadas inválidas"}})
async def add_visual_pin_comment(
    post_id: UUID, 
    request: CommentCreateRequest, 
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Registra fisicamente o Pin Visual via Caso de Uso.
    O Exception Handler Global traduz erros de domínio em respostas HTTP limpas.
    """
    # Primeiro garantimos que o post existe antes de processar lógica de domínio complexa
    repo = PostRepositorySQLAlchemy(db)
    use_case_detail = GetPostDetailUseCase(repo)
    await use_case_detail.execute(post_id) # Lança 404 se não existir via Global Handler
        
    use_case = AddCommentUseCase(repo, TimeService())
    return await use_case.execute(
        post_id=post_id,
        user_id=request.user_id,
        content=request.content,
        coord_x=request.coord_x,
        coord_y=request.coord_y
    )
