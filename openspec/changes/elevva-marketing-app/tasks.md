# Roadmap de Tarefas (Fase 2: Implementação)

Este cronograma deve seguir rigorosamente a metodologia TDD (Test-Driven Development). Nenhuma rota web pode existir antes da entidade que a governa estar testada.

## 1. Infraestrutura Docker e Configuração (TDD Nível Zero)
- [ ] 1.1 Criar o `docker-compose.yml` na raiz mapeando a topologia tripla: `db` (PostgreSQL), `api` (FastAPI) e `web` (Next.js).
- [ ] 1.2 Configurar arquivos `.env` e `.env.example` protegendo as rotas e chaves AWS/JWT.
- [ ] 1.3 Inicializar container de banco `db` e garantir conexões saudáveis no Healthcheck.

## 2. Núcleo do Domínio (TDD de Regras Puras)
- [ ] 2.1 **TDD:** Criar Suite de Testes puras (Pytest/Vitest) para a entidade `Post`, `User`, e os Objetos de Valor de `Coordinate` (X,Y).
- [ ] 2.2 **Implementação:** Codificar as lógicas e Entidades B2B independentes de banco na pasta `domain/`.
- [ ] 2.3 **TDD:** Definir os contratos das interfaces dos Repositórios para a Camada 3.

## 3. Camada de Aplicação (TDD de Casos de Uso)
- [ ] 3.1 **TDD:** Escrever testes de orquestração injetando repositórios Falsos/Mocks nos Use Cases.
- [ ] 3.2 **Implementação:** Construir a orquestração na pasta `application/` (`ApprovePostUseCase`, `UploadMediaIntentUseCase`).

## 4. Camada de Infraestrutura e Adaptadores (TDD Concreto)
- [ ] 4.1 **TDD/Implementação:** Adicionar os modelos concretos via SQLAlchemy e efetivar testes de Banco na pasta `infrastructure/`.
- [ ] 4.2 **Implementação:** Codificar o hash de Bcrypt e a liberação das Pre-signed URLs no S3.

## 5. Interface de Entrega Web (Rotas e TDD de Contrato)
- [ ] 5.1 **TDD:** Escrever testes englobando payloads do FastAPI usando `TestClient`.
- [ ] 5.2 **Implementação:** Construir as Rotas na pasta `presentation/` servindo os Endpoints HTTP consumindo o Pydantic v2.
- [ ] 5.3 **Integração E2E:** Setup Next.js com Tailwind/Shadcn UI puxando dados através dos Server Components e Polling de UI via Kanban.
