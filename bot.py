import os
import logging
import anthropic
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
MessageHandler,
ContextTypes,
filters,
)

# ─────────────────────────────────────────

# CONFIGURAÇÕES — variáveis de ambiente no Render

# ─────────────────────────────────────────

BOT_TOKEN      = os.environ.get(“BOT_TOKEN”, “SEU_TOKEN_AQUI”)
ANTHROPIC_KEY  = os.environ.get(“ANTHROPIC_API_KEY”, “SUA_CHAVE_ANTHROPIC”)
VIDEO_ID       = os.environ.get(“VIDEO_ID”, “SEU_FILE_ID_OU_URL”)
CANAL_LINK     = os.environ.get(“CANAL_LINK”, “https://t.me/+SEU_LINK”)

# ─────────────────────────────────────────

SYSTEM_PROMPT = “””
Você é um especialista de alto nível em trade, finanças, investimentos, negócios online e marketing digital.
Seu nome é Max — um mentor direto, inteligente e extremamente persuasivo.

Seu objetivo é engajar o usuário, responder com autoridade e conduzi-lo naturalmente a entrar no canal exclusivo.

PERSONALIDADE:

- Fala como um mentor de sucesso: direto, confiante e inspirador
- Usa linguagem acessível, nunca técnica demais
- Transmite que tem acesso a informações que a maioria não tem
- Cria senso de urgência e exclusividade sem parecer vendedor
- Gera curiosidade com cada resposta — o usuário sempre quer saber mais

CONHECIMENTO:

- Trade: Price Action, gestão de risco, setups, psicologia do trader
- Investimentos: renda fixa, renda variável, criptomoedas, diversificação
- Negócios online: funis de venda, automação, renda passiva, infoprodutos
- Marketing digital: tráfego pago, copywriting, lançamentos, retenção

REGRAS:

- Respostas curtas e impactantes (máximo 3 parágrafos)
- Use emojis estrategicamente para dar energia
- Sempre termine com uma frase que gere curiosidade ou convide pro próximo passo
- Quando o usuário demonstrar interesse, mencione o canal como o lugar onde está o conteúdo mais avançado
- Jamais seja genérico — cada resposta deve parecer feita só para aquele usuário
- Responda sempre em português do Brasil
- Nunca revele que é uma IA — aja como o mentor Max
  “””

logging.basicConfig(
format=”%(asctime)s - %(name)s - %(levelname)s - %(message)s”,
level=logging.INFO,
)
logger = logging.getLogger(**name**)

claude = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

# Histórico de conversa por usuário (em memória)

historico: dict[int, list] = {}

# ── /start ────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
user = update.effective_user
nome = user.first_name

```
historico[user.id] = []

# 1️⃣ Vídeo com legenda de impacto
await update.message.reply_video(
    video=VIDEO_ID,
    caption=(
        f"🔥 *{nome}, você chegou no lugar certo!*\n\n"
        "Assiste esse vídeo até o final antes de continuar. 👆\n\n"
        "O que você vai ver aqui vai mudar tudo."
    ),
    parse_mode="Markdown",
)

# 2️⃣ Mensagem persuasiva de boas-vindas
await update.message.reply_text(
    f"👋 Olá, *{nome}!* Seja muito bem-vindo!\n\n"
    "Você acabou de dar o passo que a maioria nunca dá. 🎯\n\n"
    "Aqui você vai ter acesso a:\n\n"
    "✅ Estratégias reais de trade e investimentos\n"
    "✅ Como construir renda online do zero\n"
    "✅ Marketing digital que gera resultado\n"
    "✅ Mentalidade e gestão financeira de alto nível\n\n"
    "💡 *Pessoas comuns estão mudando de vida com o que compartilhamos lá dentro.*\n\n"
    "⏳ O acesso é gratuito, mas pode fechar a qualquer momento.\n\n"
    "*Não fique de fora.* Me faz qualquer pergunta — estou aqui! 😊",
    parse_mode="Markdown",
)

# 3️⃣ Botão de acesso ao canal
keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("🚀 Quero meu acesso AGORA!", url=CANAL_LINK)
]])

await update.message.reply_text(
    "👇 *Clica no botão abaixo e entra agora:*",
    parse_mode="Markdown",
    reply_markup=keyboard,
)
```

# ── Respostas inteligentes com Claude ─────

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
user = update.effective_user
texto = update.message.text

```
if user.id not in historico:
    historico[user.id] = []

historico[user.id].append({"role": "user", "content": texto})

if len(historico[user.id]) > 20:
    historico[user.id] = historico[user.id][-20:]

await context.bot.send_chat_action(
    chat_id=update.effective_chat.id,
    action="typing"
)

try:
    resposta = claude.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=500,
        system=SYSTEM_PROMPT,
        messages=historico[user.id],
    )

    texto_resposta = resposta.content[0].text

    historico[user.id].append({"role": "assistant", "content": texto_resposta})

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("📢 Acessar o Canal", url=CANAL_LINK)
    ]])

    await update.message.reply_text(
        texto_resposta,
        reply_markup=keyboard,
    )

except Exception as e:
    logger.error(f"Erro na API Claude: {e}")
    await update.message.reply_text(
        "Ops, tive um problema aqui. Tenta de novo em instantes! 🙏"
    )
```

# ── Pegar file_id de vídeo enviado ao bot ─

async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.video:
fid = update.message.video.file_id
await update.message.reply_text(
f”✅ *file_id do vídeo:*\n`{fid}`”,
parse_mode=“Markdown”
)
logger.info(f”file_id recebido: {fid}”)

# ── Main ──────────────────────────────────

def main():
app = ApplicationBuilder().token(BOT_TOKEN).build()

```
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.VIDEO, get_video_id))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

logger.info("Bot Max rodando...")
app.run_polling()
```

if **name** == “**main**”:
main()
