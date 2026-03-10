## 1. Configuração Inicial e Infraestrutura

- [ ] 1.1 Criar repositório Git e estrutura base de diretórios (backend/ e frontend/)
- [ ] 1.2 Inicializar backend Python com FastAPI (`pip install fastapi uvicorn`)
- [ ] 1.3 Inicializar frontend com Next.js e TypeScript (`npx create-next-app@latest`)
- [ ] 1.4 Configurar banco de dados PostgreSQL e ORM (SQLModel/Alembic) no backend
- [ ] 1.5 Criar arquivo docker-compose.yml para subir o PostgreSQL localmente

## 2. Autenticação e Magic Links (Backend)

- [ ] 2.1 Criar entidades User e UserAuth (Magic Link Token) no banco de dados
- [ ] 2.2 Criar rota `POST /auth/magic-link` para gerar token JWT e enviar (mock) por email
- [ ] 2.3 Criar middleware/dependência no FastAPI para validar o token nas rotas privadas

## 3. Gestão de Calendário e Uploads (Backend)

- [ ] 3.1 Criar entidades Calendar e Post no banco de dados
- [ ] 3.2 Implementar rotas CRUD para Calendários (GET isolado por Tenant/User)
- [ ] 3.3 Implementar rotas CRUD para Publicações vinculadas a um Calendário
- [ ] 3.4 Configurar rota `POST /posts/{id}/media/upload-url` para gerar Presigned URL (AWS S3 ou Cloudinary Mock)
- [ ] 3.5 Criar rota de webhook ou endpoint de confirmação de que o upload no frontend foi bem sucedido

## 4. Gestão de Feedback e Comentários (Backend)

- [ ] 4.1 Criar entidades Comment (com coord_x, coord_y) e Idea
- [ ] 4.2 Implementar rotas de Comentários associadas a uma Publicação
- [ ] 4.3 Implementar rotas do painel Kanban de Ideias (`GET/POST /ideas`)
- [ ] 4.4 Implementar rota focada para polling `GET /posts/kanban` otimizada para listagem por status

## 5. UI/UX Base do Cliente e Agência (Frontend)

- [ ] 5.1 Configurar TailwindCSS e instalar os componentes base do Shadcn/UI
- [ ] 5.2 Criar tela de Login (`/login`) com formulário para envio de request de Magic Link
- [ ] 5.3 Criar lógica de captura do token da URL e salvamento em HttpOnly Cookie
- [ ] 5.4 Criar layout base (Sidebar de Navegação, Header com Avatar)
- [ ] 5.5 Desenvolver tela de Dashboard Kanban (usando Drag and Drop leve ou botões de transição)

## 6. Telas Core de Negócio (Frontend)

- [ ] 6.1 Desenvolver tela do Calendário interativo para Agência (agendamento de posts)
- [ ] 6.2 Desenvolver fluxo de Upload de mídia usando a Presigned URL do backend
- [ ] 6.3 Criar tela de Detalhe da Publicação (`/publicacao/[id]`)
- [ ] 6.4 Implementar componente de **Visual Pins** (captura de X,Y no clique da imagem e renderização do Pin)
- [ ] 6.5 Integrar React Query ou SWR para polling a cada 10s no Dashboard e na view de Comentários

## 7. Deploy e Finalização DevOps

- [ ] 7.1 Escrever Testes Unitários básicos (Pytest no backend, Vitest no frontend)
- [ ] 7.2 Criar Dockerfile de produção Otimizado para o FastAPI
- [ ] 7.3 Criar Dockerfile de produção Otimizado para o Next.js
- [ ] 7.4 Configurar arquivo `.github/workflows/deploy.yml` para CI/CD automatizado
