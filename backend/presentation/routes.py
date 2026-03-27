from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID

from backend.presentation.schemas import (
    PostCreateRequest, 
    PostResponse, 
    CommentCreateRequest, 
    CommentResponse,
    PostDetailResponse,
    UploadIntentRequest,
    UploadIntentResponse
)
from backend.infrastructure.database import get_db
from backend.infrastructure.models import PostModel, CommentModel, UserModel
from backend.infrastructure.s3_service import S3CloudService
from backend.domain.entities import PostStatus
from backend.presentation.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Kanban Posts B2B"])

@router.post("/upload-intent", response_model=UploadIntentResponse, status_code=201)
async def create_upload_intent(request: UploadIntentRequest, db: AsyncSession = Depends(get_db)):
    """
    RFC 2119: Emissão Efêmera da Pre-signed URL para arquitetura Cloud-first AWS S3.
    A API interceptará a solicitação de intenção de Upload do Canvas, 
    sobrescreverá o nome falho para um UUID v4 B2B e persistirá a casca no DB 
    como 'PENDING_UPLOAD'.
    """
    s3_service = S3CloudService()
    presigned = s3_service.generate_upload_url(
        file_name=request.filename, 
        file_type=request.content_type
    )
    
    new_post = PostModel(
        calendar_id=request.calendar_id,
        media_url=presigned["file_key"],
        status=PostStatus.PENDING_UPLOAD
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
        media_url=request.media_url
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

@router.get("/{post_id}", response_model=PostDetailResponse)
async def get_post(post_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    Obtém a mídia em união relacional 'Eager' com seus Pins Visuais de feedback.
    """
    # Await nativo: Liberar a Thread do Python enquanto busca os dados
    result = await db.execute(
        select(PostModel)
        .options(selectinload(PostModel.comments))
        .where(PostModel.id == post_id)
    )
    post = result.scalars().first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Regra Domain: Postagem inválida ou apagada pelo Tenant B2B.")
    return post

@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=201)
async def add_visual_pin_comment(
    post_id: UUID, 
    request: CommentCreateRequest, 
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Registra fisicamente o Pin Visual.
    O Pydantic (Schema) garantirá silenciosamente que coord_x e coord_y nunca saiam de 0% a 100%.
    """
    # Valida se a mídia mãe (post) existe
    post_result = await db.execute(select(PostModel).where(PostModel.id == post_id))
    if not post_result.scalars().first():
        raise HTTPException(status_code=404, detail="Não é possível transfixar Pin. Post não localizado.")
        
    new_comment = CommentModel(
        post_id=post_id,
        user_id=request.user_id,
        content=request.content,
        coord_x=request.coord_x,
        coord_y=request.coord_y
    )
    
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment
