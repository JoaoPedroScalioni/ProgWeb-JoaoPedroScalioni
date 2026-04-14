import pytest
from unittest.mock import AsyncMock
from uuid import uuid4
from src.application.use_cases import GetPostDetailUseCase, AddCommentUseCase
from src.domain.entities import PostEntity, PostStatus

@pytest.mark.asyncio
async def test_get_post_detail_success():
    # Arrange: Criamos um mock do repositório
    mock_repo = AsyncMock()
    post_id = uuid4()
    expected_post = PostEntity(
        id=post_id,
        calendar_id=uuid4(),
        media_url="https://elevva.com/video.mp4",
        status=PostStatus.CRIADO
    )
    mock_repo.get_by_id.return_value = expected_post
    
    use_case = GetPostDetailUseCase(mock_repo)

    # Act: Executamos a regra de negócio
    result = await use_case.execute(post_id)

    # Assert: Validamos se a lógica funcionou
    assert result.id == post_id
    assert result.status == PostStatus.CRIADO
    mock_repo.get_by_id.assert_called_once_with(post_id)

@pytest.mark.asyncio
async def test_get_post_not_found():
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.get_by_id.return_value = None
    use_case = GetPostDetailUseCase(mock_repo)

    # Act
    result = await use_case.execute(uuid4())

    # Assert
    assert result is None

@pytest.mark.asyncio
async def test_add_comment_success():
    # Arrange
    mock_repo = AsyncMock()
    mock_time = MagicMock()
    mock_time.get_now_br.return_value = "2026-04-14T17:00:00-03:00"
    
    post_id = uuid4()
    user_id = uuid4()
    comment_content = "Corrigir cor do botão"
    
    from src.domain.entities import CommentEntity
    expected_comment = CommentEntity(
        id=uuid4(),
        post_id=post_id,
        user_id=user_id,
        content=comment_content,
        coord_x=50.5,
        coord_y=60.2,
        created_at="2026-04-14T17:00:00-03:00"
    )
    mock_repo.save_comment.return_value = expected_comment
    use_case = AddCommentUseCase(mock_repo, mock_time)

    # Act
    result = await use_case.execute(
        post_id=post_id,
        user_id=user_id,
        content=comment_content,
        coord_x=50.5,
        coord_y=60.2
    )

    # Assert
    assert result.content == comment_content
    assert result.coord_x == 50.5
    mock_repo.save_comment.assert_called_once()

@pytest.mark.asyncio
async def test_add_comment_negative_coordinates():
    # Arrange
    mock_repo = AsyncMock()
    mock_time = MagicMock()
    use_case = AddCommentUseCase(mock_repo, mock_time)

    # Act & Assert
    from src.domain.exceptions import InvalidCoordinateError
    with pytest.raises(InvalidCoordinateError):
        await use_case.execute(
            post_id=uuid4(),
            user_id=uuid4(),
            content="Erro",
            coord_x=-1.0,
            coord_y=50.0
        )
