from dataclasses import dataclass, field
from uuid import UUID, uuid4
from enum import Enum

class UserRole(Enum):
    AGENCY = "AGENCY"
    CLIENT = "CLIENT"

class PostStatus(Enum):
    PENDING_UPLOAD = "PENDING_UPLOAD"
    CRIADO = "CRIADO"
    AGUARDANDO_APROVACAO = "AGUARDANDO_APROVACAO"
    APROVADO = "APROVADO"
    REJEITADO = "REJEITADO"

@dataclass
class Coordinate:
    """
    Value Object representando o Pin Visual em coordenadas fluídas (X,Y)
    """
    x: float
    y: float

@dataclass
class User:
    """
    Entidade Raiz do Multi-Tenant B2B. Isolada de qualquer framework ou banco.
    """
    name: str
    email: str
    password_hash: str
    role: UserRole
    id: UUID = field(default_factory=uuid4)

@dataclass
class Post:
    """
    Entidade Raiz do Kanban. Mantém o Link S3 e o Motor de Estados.
    """
    calendar_id: UUID
    media_url: str
    status: PostStatus = PostStatus.CRIADO
    id: UUID = field(default_factory=uuid4)

@dataclass
class Comment:
    """
    Entidade do Fluxo de Feedback Visual, agregando a Coordenada X,Y do Pin B2B ao Post do Kanban.
    """
    post_id: UUID
    user_id: UUID
    content: str
    coord: Coordinate
    id: UUID = field(default_factory=uuid4)
