import asyncio
from backend.infrastructure.security import PasswordHasher
from backend.infrastructure.database import AsyncSessionLocal
from backend.infrastructure.models import UserModel, PostModel, CalendarModel
from backend.domain.entities import UserRole, PostStatus

async def seed():
    async with AsyncSessionLocal() as db:
        print("Iniciando inserção de dados de seed...")
        
        # Criação do usuário admin
        admin = UserModel(
            name='Joao Admin',
            email='admin@elevva.com',
            password_hash=PasswordHasher.hash('admin123'),
            role=UserRole.AGENCY
        )
        db.add(admin)
        await db.flush()  # Para obter o admin.id gerado
        
        # O modelo Post requer um calendário atrelado em models.py
        calendar = CalendarModel(
            client_id=admin.id,
            month="Mês de Teste"
        )
        db.add(calendar)
        await db.flush()

        # Criação do Post de exemplo - Baseado no PostModel real (sem title/description)
        post = PostModel(
            calendar_id=calendar.id,
            media_url='https://storage.elevva.com/campanha-de-teste.mp4',
            status=PostStatus.CRIADO
        )
        db.add(post)
        
        await db.commit()
        print("✅ Usuário admin@elevva.com e Post 'Campanha de Teste' criados com sucesso!")

if __name__ == "__main__":
    asyncio.run(seed())
