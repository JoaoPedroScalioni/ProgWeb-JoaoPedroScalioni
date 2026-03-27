from uuid import UUID
from backend.domain.entities import PostStatus
from backend.domain.repositories import PostRepository

class ApprovePostUseCase:
    """Implementa o fluxo de aprovação do Kanban B2B sem conhecer SQLAlchemy"""
    
    def __init__(self, post_repo: PostRepository):
        # Injeção de Dependência abstrata 
        self.post_repo = post_repo

    def execute(self, post_id: UUID) -> bool:
        post = self.post_repo.get_by_id(post_id)
        if not post:
            raise ValueError("Erro 404: Post não encontrado no sistema")
        
        # Validação do Motor de Estados Kanban da Agência
        if post.status == PostStatus.APROVADO:
            raise ValueError("Violação de Estado: O Post já está chancelado como Aprovado pelo cliente")
            
        post.status = PostStatus.APROVADO
        self.post_repo.save(post)
        return True


class UploadMediaIntentUseCase:
    """Gerencia a emissão blindada de Pre-Signed URLs para barrar vídeos massivos"""
    
    def __init__(self, s3_service):
        # Injeta um contrato abstrato do serviço de nuvem
        self.s3_service = s3_service
        
    def execute(self, client_id: UUID, file_name: str, file_size_mb: int) -> str:
        # Proteção ativa da Memória RAM da Instância FastAPI (Limite RFC 2119 documentado)
        if file_size_mb > 500:
            raise ValueError("Bloqueio de Infraestrutura: Arquivo excede limite rígido Cloud-First de 500MB")
            
        # Delega ao adaptador de infra a geração criptográfica do token
        return self.s3_service.generate_presigned_url(client_id, file_name)
