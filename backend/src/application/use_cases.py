from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from backend.src.infrastructure.models import PostModel, CommentModel
from backend.src.domain.entities import PostEntity, CommentEntity

class GetPostDetailUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, post_id: UUID) -> PostEntity:
        # 1. Busca no Banco (Infra)
        result = await self.db.execute(
            select(PostModel)
            .options(selectinload(PostModel.comments))
            .where(PostModel.id == post_id)
        )
        post_model = result.scalars().first()
        
        if not post_model:
            return None

        # 2. Converte o modelo do banco para a nossa Entidade Pura (Domain)
        # O 'from_attributes=True' do Pydantic faz a mágica de ler o objeto do SQLAlchemy
        return PostEntity.model_validate(post_model, from_attributes=True)

class AddCommentUseCase:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, post_id: UUID, user_id: UUID, content: str, coord_x: float, coord_y: float) -> CommentEntity:
        # 1. Cria o modelo de banco
        new_comment = CommentModel(
            post_id=post_id,
            user_id=user_id,
            content=content,
            coord_x=coord_x,
            coord_y=coord_y
        )
        
        # 2. Salva na Infraestrutura
        self.db.add(new_comment)
        await self.db.commit()
        await self.db.refresh(new_comment)

        # 3. Retorna a Entidade de Domínio
        return CommentEntity.model_validate(new_comment, from_attributes=True)
