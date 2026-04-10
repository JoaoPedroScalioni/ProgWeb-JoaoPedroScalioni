import pytest
from uuid import uuid4
from backend.src.domain.entities import Post, PostStatus
from backend.src.domain.repositories import PostRepository
from backend.src.application.use_cases import GetPostDetailUseCase # Note: ApprovePostUseCase pode estar faltando/renomeado

# ==========================================
# 1. Criação dos MOCKS (In-Memory Adapters)
# ==========================================
class MockPostRepository(PostRepository):
    def __init__(self):
        self.db = {} # Simulando BD PostgreSQL
        
    def get_by_id(self, post_id):
        return self.db.get(post_id)
        
    def save(self, post):
        self.db[post.id] = post

    async def save_comment(self, comment):
        pass

class MockS3Service:
    def generate_presigned_url(self, client_id, file_name):
        return f"https://elevva-marketing-bucket.s3.amazonaws.com/temp/{client_id}/{file_name}?token=MOCK_SAFE"

# ==========================================
# 2. Ciclo TDD Refinado
# ==========================================
def test_kanban_transition_approve_post_success():
    """Valida a transição restrita AGUARDANDO -> APROVADO via Use Case"""
    repo = MockPostRepository()
    post = Post(calendar_id=uuid4(), media_url="video.mp4")
    post.status = PostStatus.AGUARDANDO_APROVACAO
    repo.save(post)
    
    use_case = ApprovePostUseCase(post_repo=repo)
    result = use_case.execute(post.id)
    
    assert result is True
    assert repo.get_by_id(post.id).status == PostStatus.APROVADO

def test_s3_upload_blocks_files_over_500mb():
    """Garante que falharemos se a agência submeter um vídeo que quebre o servidor"""
    s3_mock = MockS3Service()
    use_case = UploadMediaIntentUseCase(s3_service=s3_mock)
    
    with pytest.raises(ValueError, match="excede limite"):
        # Uma tentativa de enviar 600MB MUST levantar um erro imiediato
        use_case.execute(client_id=uuid4(), file_name="pesado.mp4", file_size_mb=600)

def test_s3_upload_emits_valid_token():
    """Verifica se o token Cloud-first está compondo a URL corretamente"""
    s3_mock = MockS3Service()
    use_case = UploadMediaIntentUseCase(s3_service=s3_mock)
    
    client_uuid = uuid4()
    url = use_case.execute(client_id=client_uuid, file_name="leve.mp4", file_size_mb=200)
    
    assert "token=MOCK_SAFE" in url
    assert str(client_uuid) in url
