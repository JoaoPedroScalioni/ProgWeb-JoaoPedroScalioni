from datetime import datetime
import pytz
from backend.src.infrastructure.config import settings

class TimeService:
    """Serviço centralizado para gestão de fuso horário America/Sao_Paulo (GMT-3)"""
    
    @staticmethod
    def get_now() -> datetime:
        """Retorna o horário atual injetado com o fuso horário configurado no settings"""
        tz = pytz.timezone(settings.TIMEZONE)
        return datetime.now(tz)

    @staticmethod
    def to_local(dt: datetime) -> datetime:
        """Converte um datetime (geralmente UTC do banco) para o fuso local configurado"""
        if dt.tzinfo is None:
            # Assume que se não tem tz, é UTC vindo do banco
            dt = pytz.utc.localize(dt)
        
        tz = pytz.timezone(settings.TIMEZONE)
        return dt.astimezone(tz)
