# Proposal: Elevva Marketing App

## Context

A empresa Elevva Marketing precisa de um sistema para facilitar o gerenciamento de publicações e a comunicação com clientes, evitando o uso do WhatsApp. O sistema funcionará como um calendário de publicações.

## Problem

A comunicação atual via WhatsApp com os clientes causa desorganização nas aprovações de postagens, impossibilitando um fluxo de trabalho estruturado para feedbacks e ideias de campanhas.

## Proposed Solution

Criar uma aplicação web baseada no modelo Cliente-Servidor (conforme os requisitos da disciplina) utilizando Clean Architecture e Domain Driven Design (DDD) no backend (FastAPI).

A aplicação terá as seguintes funcionalidades:
- **Painel de Calendário**: Calendários separados por cliente/marca onde a empresa pode agendar publicações por dia e horário.
- **Visualização Kanban**: Status claros no dashboard (ex: "Aguardando Aprovação", "Aprovado", "Pausado").
- **Upload de Mídias e Links**: Suporte a envio de imagens, vídeos e inserção de URLs atrelados às publicações do calendário.
- **Sistema Especialista de Feedback**: Fluxo de aprovação diretamente na publicação com **Pins de Comentários Visuais** (cliente pode clicar em pontos específicos da imagem/vídeo para comentar, similar ao Figma).
- **Mural de Ideias (Kanban-style)**: Uma área dedicada, visualmente estruturada como cartões (Trello-like), para clientes enviariem sugestões que a agência pode converter em publicações reais.
- **Controle de Acesso via Magic Links**: Clientes são convidados via e-mail e fazem login simplificado (sem senha) através de links clicáveis que os direcionam direto para o post que precisa de aprovação.
- **Notificações Inteligentes**: Sistema de alertas configurável, permitindo envios em tempo real ou resumos diários (Digests) unificados.

## Goals

- Centralizar e organizar a comunicação entre a Elevva Marketing e seus clientes.
- Eliminar o uso de aplicativos de mensagens genéricos (WhatsApp) para aprovação de publicações.
- Prover um histórico rastreável de feedback em publicações.
- Implementar um sistema seguro e particionado, garantindo que clientes visualizam somente os calendários designados a eles.

## Non-Goals

- Integração direta de postagens automáticas em redes sociais por meio de suas APIs (neste momento, o foco é aprovação interna).
- Edição complexa de multimídia (imagens/vídeos) dentro da plataforma.
