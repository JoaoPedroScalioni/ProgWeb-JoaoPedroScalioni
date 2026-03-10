# Design: Elevva Marketing App

## Architecture

O sistema utilizará o modelo **Cliente-Servidor**, dividido em duas aplicações principais (seguindo as diretrizes da disciplina):
1. **Backend (Servidor)**: Desenvolvido em **Python com FastAPI**. A arquitetura interna seguirá os princípios de **Clean Architecture** e **Domain Driven Design (DDD)**.
2. **Frontend (Cliente)**: Desenvolvido em **TypeScript com Next.js** (App Router, Server and Client Side Rendering), utilizando as bibliotecas **TailwindCSS** e **Shadcn/UI** para a interface.

Toda a infraestrutura será containerizada utilizando **Docker** (para desenvolvimento e deploy).

## Components

### Backend (Clean Architecture)
- **Domain Layer**: Entidades de negócio puro (Empresa, Cliente, Calendário, Publicação, Comentário, Ideia).
- **Use Cases (Application Layer)**: Regras de negócio orquestradas (ex: `AgendarPublicacao`, `ComentarPublicacao`, `EnviarIdeia`, `ConvidarCliente`).
- **Interface Adapters**:
  - **Controllers (FastAPI Routes)**: Endpoints REST assíncronos.
  - **Presenters/Schemas (Pydantic)**: Validação e formatação de dados de entrada e saída (OpenAPI integrável futuramente via Swagger).
- **Frameworks & Drivers**:
  - **Banco de Dados**: PostgreSQL com ORM (ex: SQLAlchemy ou SQLModel) + Migrations (Alembic).
  - **Pipeline de Media (Cloud First)**: Geração de URLs pré-assinadas (ex: S3 Presigned URLs) para que o frontend Next.js faça o upload direto pesado para a nuvem, mantendo o FastAPI leve e seguro.
  - **Autenticação**: JWT (JSON Web Tokens).

### Frontend (Next.js)
- **Páginas (App Router)**:
  - `/login`: Tela de autenticação separando fluxos de "Sou Agência" e "Sou Cliente" + Fluxo de Magic Link (sem senha).
  - `/dashboard`: Visão geral Kanban dos posts pendentes/aprovados/publicados.
  - `/calendario/[id]`: Visualização mês/semana/dia com as publicações agendadas.
  - `/publicacao/[id]`: Detalhe do post (Mídias, URL) com painel interativo de **Comentários visuais (Pins em coordenadas X, Y)**.
  - `/ideias`: Mural Kanban dedicado a sugestões do Cliente (Inbox -> Em Produção -> Postado).
- **Componentes Base**: Interfaces polidas com Shadcn/UI e TailwindCSS.
- **Integração de API**: Consumo da API do backend com tipagem (TypeScript integrado via OpenAPI).

## Data Model (DDD Context)

- **Usuário (User)**: `id`, `nome`, `email`, `senha_hash`, `role` (ADMIN_AGENCIA, CLIENTE).
- **Sessão / Magic Link (UserAuth)**: `token`, `usuario_id`, `expires_at` (para autenticação sem senha).
- **Calendário (Calendar)**: `id`, `nome`, `descricao`, relacional (`cliente_id`).
- **Publicação (Post)**: `id`, `calendario_id`, `data_hora`, `status` (RASCUNHO, AGUARDANDO_APROVACAO, APROVADO, PUBLICADO), `descricao`.
- **Mídia (Media)**: `id`, `publicacao_id`, `tipo` (IMAGEM, VIDEO, URL), `url_caminho`.
- **Comentário (Comment)**: `id`, `publicacao_id`, `usuario_id`, `texto`, `data_criacao`, `coord_x` (opcional), `coord_y` (opcional).
- **Ideia (Idea)**: `id`, `calendario_id`, `usuario_id`, `titulo`, `descricao`, `status` (INBOX, BACKLOG, EM_PRODUCAO, CONCLUIDO).
- **Configuração de Notificação (NotificationSettings)**: `usuario_id`, `frequencia` (REAL_TIME, DIARY_DIGEST), `eventos_inscritos`.

## API / Interface

Principais rotas (REST):
- `POST /auth/login`: Autenticação via Senha.
- `POST /auth/magic-link`: Solicitação e consumo de token sem senha.
- `GET /calendars`: Retorna a lista de calendários permitidos para o usuário logado.
- `GET /calendars/{id}/posts`: Lista publicações de um mês/semana específico.
- `GET /posts/kanban`: Lista publicações baseadas no seu status (Aguardando Aprovação, Aprovadas).
- `POST /posts`: Cria uma postagem no calendário.
- `POST /posts/{id}/media`: Faz o upload de um arquivo ou atrela URL.
- `POST /posts/{id}/comments`: Adiciona um comentário de validação (suportando coordenadas de visual pin).
- `GET /ideas` e `POST /ideas`: Gerenciamento do painel de opiniões (estilo Trello/Kanban).

## Risks / Trade-offs

- **Cloud Upload Pipeline**: Fazer upload direto do Next.js para a nuvem por Presigned URLs exige boa configuração de CORS no Bucket (S3/Azure). Porém, compensa pois evita que o container do FastAPI fique sem memória ao processar vídeos de 500MB de campanhas da agência.
- **Sincronismo de Notificações**: O envio de e-mails em tempo real pode travar o request. Isso deve ser jogado para uma fila de processamento assíncrono (ex: Background Tasks do FastAPI ou Celery) para garantir resposta rápida ao usuário.
