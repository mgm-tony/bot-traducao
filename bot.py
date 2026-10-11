import os
import logging

import discord
from discord import app_commands
from discord.ext import commands
import deepl

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("translator_bot")

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

if not DISCORD_TOKEN:
    raise RuntimeError("A variável de ambiente DISCORD_TOKEN não foi configurada.")
if not DEEPL_API_KEY:
    raise RuntimeError("A variável de ambiente DEEPL_API_KEY não foi configurada.")

translator = deepl.Translator(DEEPL_API_KEY)

# Adicione aqui os IDs dos servidores para sincronizar os comandos quase imediatamente.
# Exemplo no Railway: DISCORD_GUILD_ID=123456789012345678
GUILD_ID = os.getenv("DISCORD_GUILD_ID")


class TranslatorBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            log.info("Comandos sincronizados no servidor %s", GUILD_ID)
        else:
            await self.tree.sync()
            log.info("Comandos globais sincronizados; a propagação pode demorar.")

    async def on_ready(self):
        log.info("Bot conectado como %s (ID: %s)", self.user, self.user.id)


bot = TranslatorBot()


def translate_text(text: str, target_lang: str) -> str:
    """Executa a chamada síncrona ao DeepL."""
    result = translator.translate_text(text, target_lang=target_lang)
    return str(result)


async def send_translation(interaction: discord.Interaction, text: str, target_lang: str):
    if not text.strip():
        await interaction.response.send_message(
            "Informe algum texto para traduzir.", ephemeral=True
        )
        return

    await interaction.response.defer(ephemeral=True, thinking=True)

    try:
        translated = await bot.loop.run_in_executor(
            None, translate_text, text, target_lang
        )
    except Exception:
        log.exception("Falha ao traduzir texto")
        await interaction.followup.send(
            "Não consegui traduzir essa mensagem. Verifique a chave da API, "
            "o limite de uso e tente novamente.",
            ephemeral=True,
        )
        return

    # O limite das mensagens do Discord é 2000 caracteres.
    header = f"**Tradução ({target_lang.upper()})**\n"
    chunks = []
    remaining = translated
    first_limit = 2000 - len(header)

    chunks.append(header + remaining[:first_limit])
    remaining = remaining[first_limit:]

    while remaining:
        chunks.append(remaining[:2000])
        remaining = remaining[2000:]

    await interaction.followup.send(chunks[0], ephemeral=True)
    for chunk in chunks[1:]:
        await interaction.followup.send(chunk, ephemeral=True)


@bot.tree.command(name="translate", description="Traduz um texto para outro idioma.")
@app_commands.describe(
    idioma="Código do idioma de destino, por exemplo: ru, en, pt-BR, ja ou ko",
    texto="Texto que deseja traduzir",
)
@app_commands.rename(idioma="idioma", texto="texto")
async def translate_command(
    interaction: discord.Interaction,
    idioma: str,
    texto: str,
):
    """Slash command privado: /translate idioma:ru texto:..."""
    # O DeepL usa códigos como RU, EN-US, PT-BR, JA, KO.
    target = idioma.strip().upper().replace("_", "-")
    await send_translation(interaction, texto, target)


@bot.tree.context_menu(name="Traduzir mensagem")
async def translate_message_context(interaction: discord.Interaction, message: discord.Message):
    """Menu de contexto: clique com o botão direito numa mensagem."""
    # O menu pergunta o idioma de destino por meio de uma resposta inicial.
    # Para manter o uso simples e privado, esta ação traduz para português.
    await send_translation(interaction, message.content, "PT-BR")


@bot.event
async def on_error(event, *args, **kwargs):
    log.exception("Erro não tratado no evento %s", event)


bot.run(DISCORD_TOKEN)
