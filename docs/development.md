# Guia de Desenvolvimento

Este guia orienta o processo de desenvolvimento local do TDAH App, desde a preparação do ambiente até a execução de testes.

## Pré-requisitos

1. Instale as ferramentas da stack escolhida (por exemplo, Flutter SDK, Android Studio/Xcode, Node.js para ferramentas auxiliares).
2. Configure um emulador ou dispositivo físico para testes.
3. Garanta que você tenha acesso aos serviços externos listados em `.env.example`.

## Configuração inicial

```bash
cp .env.example .env
# Edite o arquivo com os valores reais
```

- Atualize as chaves API e tokens conforme o ambiente (desenvolvimento, homologação, produção).
- Documente novas variáveis em `.env.example` para manter a paridade entre ambientes.

## Fluxo de trabalho sugerido

1. Crie uma branch a partir da `main` (por exemplo, `feature/nome-da-funcionalidade`).
2. Implemente a funcionalidade seguindo as diretrizes de arquitetura.
3. Execute os testes automatizados antes de abrir o pull request.
4. Utilize commits pequenos e descritivos.

## Qualidade e testes

- **Testes unitários**: adote a ferramenta padrão da stack (por exemplo, `flutter test`).
- **Testes de integração**: defina cenários críticos e automatize sempre que possível.
- **Lint e formatação**: configure scripts de lint (como `flutter analyze` ou `dart format --output=none --set-exit-if-changed`).

Documente neste arquivo comandos adicionais que o time adotar, como scripts personalizados ou ferramentas de inspeção estática.

## Observabilidade em desenvolvimento

- Configure logging estruturado para facilitar a depuração.
- Utilize ferramentas de monitoramento (por exemplo, Firebase Crashlytics, Sentry) em modo sandbox para validar a integração.

## Checklist antes do PR

- [ ] Código compilando sem warnings críticos.
- [ ] Testes automatizados executados e aprovados.
- [ ] Documentação atualizada (README, ADRs, comentários em código).
- [ ] Screenshots ou gravações de tela anexadas quando aplicável.

Seguir este guia garante que as contribuições mantenham um padrão de qualidade consistente e facilita a revisão técnica.
