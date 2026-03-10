# Specifications: Elevva Marketing App

## Core Capabilities

### 1. Sistema Especialista de Comentários Visuais (Pins X,Y)
Permite que o cliente interaja com precisão de pixel no post enviado pela agência.

- **DADO QUE** o cliente acessa a página de aprovação de um post via Dashboard.
- **QUANDO** ele clica em qualquer ponto da visualização principal da Mídia (Imagem ou Vídeo renderizado).
- **ENTÃO** um formulário pop-up deve abrir para capturar o texto do comentário.
- **E** a interface deve renderizar visualmente uma marcação ("Pin") nas coordenadas percentuais (X,Y) do clique relativo à dimensão original do container da imagem.

### 2. Autenticação Simplificada B2B (Magic Links)
Fornece um método sem fricção para aprovação de conteúdo sem exigir que clientes lembrem de senhas.

- **DADO QUE** um cliente existe no banco de dados e não possui senha associada.
- **QUANDO** ele insere seu email na tela de login (`/login`) ou clica diretamente em um link recebido por email (`/auth/magic-link?token=XYZ`).
- **ENTÃO** a API (FastAPI) valida o token JWT.
- **E** (caso token seja válido), o cliente é redirecionado pro Client Dashboard com uma sessão HTTP-Only válida para aquele Tenant (separação de dados).

### 3. Pipeline de Armazenamento Cloud-First
Garante performance e não-bloqueio do servidor FastAPI durante envio de gigabytes de conteúdo multimídia da agência.

- **DADO QUE** a Agência deseja realizar upload de um vídeo de campanha de 200MB.
- **QUANDO** o upload inicia no Dashboard da Agência.
- **ENTÃO** o Frontend (Next.js) realiza um `POST` solicitando uma URL Pré-assinada (S3/Azure) pro FastAPI.
- **E** recebe de volta a URL com token de permissão de escrita temporária.
- **ENTÃO** o Frontend transmite binariamente (PUT) o arquivo de 200MB *diretamente* ao serviço de Cloud.
- **E** (on success), notifica o FastAPI da existência do novo arquivo para linkar à postagem com um registro leve no banco de dados.

### 4. Kanban de Aprovações Orientado a Polling (SWR)
Permite atualizações ágeis e near real-time do andamento das aprovações sem as dores de infraestrutura de WebSockets.

- **DADO QUE** o Analista da Elevva está com o Dashboard de um Cliente ativo na tela.
- **E** o Cliente finalizou a aprovação em seu próprio computador, alterando o status no backend.
- **QUANDO** a biblioteca do frontend (ex: React Query) dispara seu Polling de janela visível (intervalo de 10s).
- **ENTÃO** O App busca levemente via `GET` na rota de status atual.
- **E** O card Kanban transita animadamente da coluna "Aguardando Aprovação" para "Aprovado" instantaneamente na tela do analista.

### 5. Mural de Ideias Isolado (Backlog Colaborativo)
Funciona como um Inbox para sugestões do cliente final, que podem ser promovidas à pauta de trabalho internamente.

- **DADO QUE** um cliente tem ideias fora da grade estabelecida do calendário.
- **QUANDO** ele preenche um novo card no `/ideias`.
- **ENTÃO** a entrada é listada no "Inbox" do cliente e da agência.
- **E** a Agência pode mover esse card numa interface Kanban (Trabalhando, Rejeitado, Promovido a Post).
