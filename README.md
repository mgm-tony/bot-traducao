# Bot tradutor para Discord (Python + DeepL)

O bot oferece:
- `/translate idioma texto`: traduz o texto informado.
- Menu de contexto **Traduzir mensagem**: traduz a mensagem selecionada para português (PT-BR).
- Respostas ephemeral: a tradução só é visível para a pessoa que executou a interação.

## Arquivos
- `bot.py`: código do bot.
- `requirements.txt`: dependências Python.
- `Procfile`: comando de inicialização para serviços Railway do tipo worker.
- `.env.example`: nomes das variáveis de ambiente (não contém chaves reais).
- `.gitignore`: evita enviar arquivos locais e segredos ao GitHub.

## Configurar o bot no Discord
1. Crie uma aplicação no Discord Developer Portal e adicione um bot.
2. Copie o token do bot e guarde-o em local privado.
3. Em OAuth2 > URL Generator, selecione os escopos `bot` e `applications.commands`.
4. Gere a URL e convide o bot ao servidor.
5. Não publique o token no GitHub nem o envie em chats.

## Configurar o DeepL
1. Crie/acesse uma conta com acesso à DeepL API.
2. Copie a chave da API (não a senha da conta).
3. Confira se o plano permite o uso pretendido e se há limites/custos aplicáveis.

## Implantar no Railway
1. Envie os arquivos deste projeto para um repositório do GitHub.
2. No Railway, crie um projeto e implante a partir desse repositório.
3. Configure o serviço como worker se a interface permitir; o `Procfile` define `python bot.py`.
4. Em Variables, crie `DISCORD_TOKEN` e `DEEPL_API_KEY`.
5. Opcionalmente, defina `DISCORD_GUILD_ID` com o ID do servidor para sincronizar os comandos de teste rapidamente.
6. Consulte os logs do serviço para verificar se o bot iniciou corretamente.

Sem `DISCORD_GUILD_ID`, os comandos globais podem demorar para aparecer. Para testes, é recomendável definir o ID do servidor.

## Usar o comando
No Discord, use `/translate` e preencha:
- `idioma`: por exemplo `RU`, `EN-US`, `PT-BR`, `JA` ou `KO`.
- `texto`: o texto a traduzir.

A interação do slash command não é publicada como uma mensagem normal no canal; a resposta do bot é ephemeral.

## Observações importantes
- O menu de contexto traduz para português brasileiro por padrão. Para escolher o idioma no menu de contexto, será necessário adicionar um fluxo interativo de seleção.
- O código usa a DeepL API. Nem todos os códigos de idioma são necessariamente aceitos em todos os planos/versões; consulte a documentação atual da DeepL API.
- A API pode impor limites de caracteres, disponibilidade e cobrança.
- Evite registrar tokens/chaves nos logs e nunca os inclua no repositório.
