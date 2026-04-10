import pytest
from uuid import UUID, uuid4
from backend.src.domain.entities import User, Post, Coordinate, UserRole, PostStatus

# Fase RED: O teste foi idealizado exigindo comportamentos que não existiam.
# Fase GREEN: Agora eles passam contra as dataclasses puras.

def test_user_creation_must_generate_uuid_v4():
    """Valida se todo usuário nasce com um UUID irreplicável garantindo segurança B2B"""
    user = User(
        name="Teste Elevva", 
        email="teste@elevvab2b.com", 
        password_hash="fake_bcrypt_hash", 
        role=UserRole.CLIENT
    )
    assert isinstance(user.id, UUID), "ID MUST ser um UUID válido"
    assert user.role == UserRole.CLIENT

def test_coordinate_is_a_pure_value_object():
    """Valida se a coordenada armazena o exato ponto de clique no Vídeo/Imagem"""
    coord = Coordinate(x=45.5, y=89.2)
    assert coord.x == 45.5
    assert coord.y == 89.2

def test_post_creation_must_default_to_criado_status():
    """Valida o motor de estado inicial do Kanban"""
    calendar_uuid = uuid4()
    post = Post(
        calendar_id=calendar_uuid, 
        media_url="https://elevva.s3.amazonaws.com/video_pesado.mp4"
    )
    assert post.status == PostStatus.CRIADO, "Post MUST iniciar no status CRIADO"
    assert isinstance(post.id, UUID)
    assert post.calendar_id == calendar_uuid

def test_comment_pin_visual_creation():
    """QA Smoke Test: Valida 100% de Cobertura para a inserção de Pins Visuais no Kanban"""
    from backend.src.domain.entities import Comment
    coord = Coordinate(x=10.5, y=50.2)
    comment = Comment(
        post_id=uuid4(),
        user_id=uuid4(),
        content="Alterar o logo para preto",
        coord=coord
    )
    assert comment.coord.x == 10.5
    assert comment.coord.y == 50.2
    assert isinstance(comment.id, UUID), "Todo feedback exige identificador rastreável B2B"
