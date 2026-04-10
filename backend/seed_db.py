import asyncio
from sqlalchemy import delete
from backend.src.infrastructure.security import PasswordHasher
from backend.src.infrastructure.database import AsyncSessionLocal
from backend.src.infrastructure.models import UserModel, PostModel, CalendarModel, CommentModel
from backend.src.domain.entities import UserRole, PostStatus
from backend.src.infrastructure.utils.time_service import TimeService

async def seed():
    async with AsyncSessionLocal() as db:
        print("🚀 Iniciando Seeding Narrativo: Elevva Marketing (Storytelling Mode)...")
        
        # 1. Limpeza Idempotente (Ordem reversa de dependência)
        print("🧹 Limpando dados antigos para garantir estado limpo...")
        await db.execute(delete(CommentModel))
        await db.execute(delete(PostModel))
        await db.execute(delete(CalendarModel))
        await db.execute(delete(UserModel))
        
        # 2. Usuários (Narrativa: Agência Joao e Cliente Mayane)
        print("👤 Criando Personagens da Campanha...")
        agency = UserModel(
            name='João Pedro (Agência Elevva)',
            email='joao@elevva.com',
            password_hash=PasswordHasher.hash('elevva2026'),
            role=UserRole.AGENCY,
            created_at=TimeService.get_now()
        )
        client = UserModel(
            name='Mayane (Diretora de Marca)',
            email='mayane@cliente.com',
            password_hash=PasswordHasher.hash('cliente123'),
            role=UserRole.CLIENT,
            created_at=TimeService.get_now()
        )
        db.add_all([agency, client])
        await db.flush()

        # 3. Calendário (Narrativa: Coleção de Lançamento Abr/2026)
        print("📅 Criando Calendário: Lançamento Coleção Outono 2026...")
        calendar = CalendarModel(
            client_id=client.id,
            month="Abril/2026 - Lançamento Outono"
        )
        db.add(calendar)
        await db.flush()

        # 4. Posts (Mídias no pipeline Kanban)
        print("🎬 Gerando Mídias no Pipeline...")
        post_video = PostModel(
            calendar_id=calendar.id,
            media_url='https://storage.elevva.com/campanha-video-outono.mp4',
            status=PostStatus.AGUARDANDO_APROVACAO,
            created_at=TimeService.get_now()
        )
        post_foto = PostModel(
            calendar_id=calendar.id,
            media_url='https://storage.elevva.com/foto-look-01.jpg',
            status=PostStatus.CRIADO,
            created_at=TimeService.get_now()
        )
        db.add_all([post_video, post_foto])
        await db.flush()

        # 5. Pins Visuais (Feedback real da Janela de Aprovação)
        print("📍 Transfixando Pins Visuais (Feedbacks)...")
        pin1 = CommentModel(
            post_id=post_video.id,
            user_id=client.id,
            content="Mayane: O logotipo no canto superior está muito pequeno, precisa de mais destaque.",
            coord_x=12.5,
            coord_y=15.0,
            created_at=TimeService.get_now()
        )
        pin2 = CommentModel(
            post_id=post_video.id,
            user_id=agency.id,
            content="João (Agência): Ajuste de brilho necessário no frame 05.",
            coord_x=85.0,
            coord_y=42.5,
            created_at=TimeService.get_now()
        )
        db.add_all([pin1, pin2])
        
        await db.commit()
        print("\n" + "="*50)
        print("✅ SEEDING CONCLUÍDO COM SUCESSO!")
        print(f"📧 Login Agency: joao@elevva.com / elevva2026")
        print(f"📧 Login Client: mayane@cliente.com / cliente123")
        print("="*50)

if __name__ == "__main__":
    asyncio.run(seed())
