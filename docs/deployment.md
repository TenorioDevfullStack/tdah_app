# Guia de Deploy

Este guia documenta o processo para publicar o TDAH App em produção. Adapte os passos conforme a stack da aplicação.

## Preparação

1. Garanta que o `main` esteja atualizado com as últimas mudanças aprovadas.
2. Verifique o checklist de QA em `docs/development.md`.
3. Confirme que o arquivo `.env` possui as credenciais de produção (nunca faça commit delas).

## Build de produção

### Flutter (exemplo)

```bash
flutter clean
flutter pub get
flutter build apk --release
flutter build appbundle --release
flutter build ios --release
```

- Certifique-se de que as assinaturas Android (keystore) e iOS (certificados e perfis) estejam configuradas em um cofre seguro.
- Versione apenas os artefatos necessários para publicação em lojas (Google Play / App Store) por meio de pipelines, não diretamente no repositório.

## Automação e CI/CD

- Configure um pipeline (por exemplo, GitHub Actions, Bitrise, Codemagic) para executar testes e builds automatizados.
- Utilize variáveis de ambiente ou secrets no provedor de CI para armazenar credenciais sensíveis.
- Gere changelog automaticamente a partir das mensagens de commit ou PRs para acompanhar releases.

## Publicação

1. Faça upload dos artefatos assinados para as lojas oficiais ou distribua via MDM.
2. Valide as métricas de monitoramento e logs após o lançamento.
3. Atualize a documentação e registre a versão liberada (ex.: `v1.0.0`).

## Pós-deploy

- Monitore erros e performance por meio das ferramentas configuradas (Sentry, Crashlytics, etc.).
- Recolha feedback dos usuários e priorize ajustes para a próxima iteração.
- Atualize `docs/architecture.md` e `docs/development.md` se novas decisões surgirem durante o deploy.

Seguindo estas orientações o processo de publicação fica previsível e rastreável, reduzindo riscos durante releases.
