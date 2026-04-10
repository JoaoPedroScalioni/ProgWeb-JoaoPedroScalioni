from abc import ABC, abstractmethod
from uuid import UUID
from backend.src.domain.entities import PostEntity, CommentEntity

class PostRepository(ABC):
    @abstractmethod
    async def get_by_id(self, post_id: UUID) -> PostEntity:
        pass

    @abstractmethod
    async def save(self, post: PostEntity) -> PostEntity:
        pass

    @abstractmethod
    async def save_comment(self, comment: CommentEntity) -> CommentEntity:
        pass

class StorageRepository(ABC):
    @abstractmethod
    def generate_upload_url(self, file_name: str, file_type: str) -> dict:
        """Contrato para geração de URL de upload (S3, Local, etc)"""
        pass
