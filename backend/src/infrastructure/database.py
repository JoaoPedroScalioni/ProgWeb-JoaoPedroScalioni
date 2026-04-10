from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from backend.src.infrastructure.config import settings
from backend.src.infrastructure.storage_impl import S3StorageRepository

# Engine Assíncrona para Alta Escala (Não trava o Servidor Web enquanto o Banco processa)
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Maker que gerará a sessão temporária injetada pelo Depends
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    """Dependency Injection: Fornece e encerra sessões UUID isoladas para cada Requisição HTTP via Yield"""
    async with AsyncSessionLocal() as session:
        yield session

def get_storage():
    """Fornece o Adaptador de Storage concreto (S3 por padrão)"""
    return S3StorageRepository()
