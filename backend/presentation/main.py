from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.presentation.routes import router
from backend.presentation.auth import router as auth_router

# O coração do ciclo de vida da Aplicação B2B
app = FastAPI(
    title="Elevva Marketing App - API B2B",
    description="Motor de aprovação Kanban e visual pins com Bypass AWS S3",
    version="1.0.0"
)

# Governança de CORS para permitir restrito acesso do Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Injeção dos Roteadores Clean Architecture Elevva
app.include_router(auth_router)
app.include_router(router)

@app.get("/health")
async def health_check():
    """Rota de telemetria crua para o Load Balancer e Docker Healthcheck"""
    return {"status": "ok", "message": "Elevva API is operational."}
