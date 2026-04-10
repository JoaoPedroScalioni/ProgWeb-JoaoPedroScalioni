from uuid import UUID
from backend.src.domain.entities import PostEntity, CommentEntity
from backend.src.domain.repositories import PostRepository
from backend.src.infrastructure.utils.time_service import TimeService
from backend.src.domain.exceptions import PostNotFoundError, InvalidCoordinateError

class GetPostDetailUseCase:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def execute(self, post_id: UUID) -> PostEntity:
        post = await self.repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundError(str(post_id))
        return post

class AddCommentUseCase:
    def __init__(self, repo: PostRepository):
        self.repo = repo

    async def execute(self, post_id: UUID, user_id: UUID, content: str, coord_x: float, coord_y: float) -> CommentEntity:
        from uuid import uuid4
        
        # Regra de Negócio Sniper: Não aceitar coordenadas negativas (fora do canvas)
        if coord_x < 0 or coord_y < 0:
            raise InvalidCoordinateError("Regra B2B: As coordenadas do Pin não podem ser negativas.")
        
        comment_entity = CommentEntity(
            id=uuid4(),
            post_id=post_id,
            user_id=user_id,
            content=content,
            coord_x=coord_x,
            coord_y=coord_y,
            created_at=TimeService.get_now()
        )
        return await self.repo.save_comment(comment_entity)
