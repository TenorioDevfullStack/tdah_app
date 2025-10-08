# Decisões Arquiteturais

Este documento serve como registro das escolhas arquiteturais do TDAH App. Utilize-o como um log vivo; sempre que uma nova decisão relevante for tomada, acrescente uma entrada seguindo o formato abaixo.

## Visão do sistema

- **Alvo principal**: aplicação móvel focada em auxiliar pessoas com TDAH.
- **Plataforma**: defina aqui se o projeto utilizará Flutter, React Native ou outra tecnologia e documente as razões.
- **Serviços críticos**: liste APIs, bancos de dados, serviços de mensageria, ferramentas de analytics e demais integrações.

## Registro de ADRs

| ID | Data | Decisão | Contexto | Consequências |
|----|------|---------|----------|----------------|
| ADR-001 | YYYY-MM-DD | Descrição curta | Quais problemas levaram a essa decisão | Impactos positivos e negativos |

## Mapa de módulos

Descreva os módulos principais (por exemplo: autenticação, conteúdos educativos, acompanhamento de tarefas) e suas responsabilidades.

## Fluxos principais

- **Onboarding**: descreva telas, integrações e dados necessários para cadastrar um novo usuário.
- **Sincronização de dados**: documente como o aplicativo se comunica com o backend e como lidar com modo offline.
- **Notificações**: detalhe o mecanismo adotado (push, locais, e-mail) e como configurar os provedores.

## Padrões e boas práticas

- Defina guidelines de gerenciamento de estado, camadas de dados e organização de arquivos.
- Registre padrões de nomenclatura e convenções de commits.
- Documente bibliotecas ou pacotes que sejam obrigatórios.

Mantenha este arquivo atualizado para facilitar o onboarding de novos integrantes e preservar o conhecimento do projeto.
