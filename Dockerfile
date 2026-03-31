# 1. Imagem base leve solicitada pelo professor
FROM python:3.12-slim

# 2. Configurações para o Python não gerar arquivos inúteis (.pyc) e exibir logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Define a pasta de trabalho dentro do contêiner
WORKDIR /app

# 4. Instala dependências do sistema necessárias para o PostgreSQL (libpq-dev)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. Copia o arquivo de dependências e instala as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copia todo o código do projeto para dentro do contêiner
COPY . .

# 7. Expõe a porta que o FastAPI vai usar
EXPOSE 8000

# 8. Comando corrigido para mapear a pasta 'backend' da Clean Architecture
CMD ["uvicorn", "backend.presentation.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
