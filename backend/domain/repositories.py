from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from backend.domain.entities import Post

class PostRepository(ABC):
    """
    Contrato de Interface na Camada Domain. 
    A Clean Architecture exige que o Domínio diga O QUE ele precisa, e a Infraestrutura obedeça COMO fazer.
    """
    @abstractmethod
    def get_by_id(self, post_id: UUID) -> Optional[Post]:
        pass
    
    @abstractmethod
    def save(self, post: Post) -> None:
        pass
