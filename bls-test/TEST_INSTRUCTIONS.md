# Teste em tempo real (DEMO)

1. Compilar o EA `NewsXAU_V1_GITHUB_TEST.mq5` no MetaEditor.
2. No MT5: Ferramentas > Opções > Expert Advisors > permitir WebRequest para `https://raw.githubusercontent.com`.
3. Usar apenas uma conta DEMO.
4. O feed está em `events.json` e os horários são lidos como hora do servidor MT5.
5. Os eventos de teste são independentes do calendário económico real.

Atenção: o feed GitHub é uma fonte de teste e a latência de HTTP/CDN não é equivalente a uma fonte institucional de notícias. O teste valida o circuito de receção -> decisão -> envio da ordem.
