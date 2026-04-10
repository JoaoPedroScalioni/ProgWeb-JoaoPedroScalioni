from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from uuid import UUID
from backend.src.domain.repositories import PostRepository
from backend.src.infrastructure.models import PostModel, CommentModel
from backend.src.domain.entities import PostEntity, CommentEntity

class PostRepositorySQLAlchemy(PostRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, post_id: UUID) -> PostEntity:
        query = await self.session.execute(
            select(PostModel)
            .options(selectinload(PostModel.comments))
            .filter(PostModel.id == post_id)
        )
        post_model = query.scalars().first()
        if not post_model:
            return None
        return PostEntity.model_validate(post_model, from_attributes=True)

    async def save(self, post: PostEntity) -> PostEntity:
        # Placeholder for later implementation of saving
        pass

    async def save_comment(self, comment: CommentEntity) -> CommentEntity:
        new_comment = CommentModel(
            post_id=comment.post_id,
            user_id=comment.user_id,
            content=comment.content,
            coord_x=comment.coord_x,
            coord_y=comment.coord_y,
            created_at=comment.created_at
        )
        self.session.add(new_comment)
        await self.session.commit()
        await self.session.refresh(new_comment)
        
        return CommentEntity.model_validate(new_comment, from_attributes=True)
