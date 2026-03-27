from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.infrastructure.config import settings

# Engine Assíncrona para Alta Escala (Não trava o Servidor Web enquanto o Banco processa)
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Maker que gerará a sessão temporária injetada pelo Depends
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """Dependency Injection: Fornece e encerra sessões UUID isoladas para cada Requisição HTTP via Yield"""
    async with AsyncSessionLocal() as session:
        yield session
