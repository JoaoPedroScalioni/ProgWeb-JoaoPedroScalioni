import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from uuid import uuid4

from backend.src.interfaces.routes import router
# from backend.src.application.use_cases import ApprovePostUseCase 
from backend.tests.application.test_use_cases import MockPostRepository
from backend.src.domain.entities import Post, PostStatus

# ===============================================
# Configuração do Ambiente TestClient (TDD Contrato)
# ===============================================
app = FastAPI()
app.include_router(router)

# Massa de dados injetada in-memory
repo = MockPostRepository()
target_post_id = uuid4()
post = Post(
    id=target_post_id, 
    calendar_id=uuid4(), 
    media_url="b2b_ad.mp4",
    status=PostStatus.AGUARDANDO_APROVACAO
)
repo.save(post)

# Overriding as dependências web do FastAPI pelos Mock do TDD Fase 3
def override_use_case():
    return ApprovePostUseCase(post_repo=repo)

app.dependency_overrides[get_approve_use_case] = override_use_case
client = TestClient(app)

# ===============================================
# Execução da Validação de Contrato de API
# ===============================================
def test_approve_post_rest_contract_success():
    """Valida se uma requisição HTTP REST reflete a regra do Kanban na Clean Arch"""
    client_uuid = str(uuid4())
    response = client.post(f"/posts/{target_post_id}/approve", json={"client_id": client_uuid})
    
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert repo.get_by_id(target_post_id).status == PostStatus.APROVADO

def test_approve_post_rest_contract_http_400():
    """TDD Red: Se o cliente der um duplo-clique no Next.js chamando a API 2 vezes, a API cai com 400"""
    client_uuid = str(uuid4())
    # O post já foi Aprovado no teste anterior. Se rodar de novo:
    response = client.post(f"/posts/{target_post_id}/approve", json={"client_id": client_uuid})
    
    assert response.status_code == 400
    assert "Violação de Estado" in response.json()["detail"]
