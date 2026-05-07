import os
import logging
import google.generativeai as genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
ApplicationBuilder,
CommandHandler,
MessageHandler,
ContextTypes,
filters,
)

BOT_TOKEN    = os.environ.get(“BOT_TOKEN”, “”)
GEMINI_KEY   = os.environ.get(“GEMINI_API_KEY”, “”)
VIDEO_ID     = os.environ.get(“VIDEO_ID”, “”)
CANAL_LINK   = os.environ.get(“CANAL_LINK”, “https://t.me/+SEU_LINK”)

SYSTEM_PROMPT = (
“Voce e um especialista de alto nivel em trade, financas, investimentos, negocios online e marketing digital. “
“Seu nome e Max, um mentor direto, inteligente e extremamente persuasivo. “
“Seu objetivo e engajar o usuario, responder com autoridade e conduzi-lo naturalmente a entrar no canal exclusivo. “
“PERSONALIDADE: Fala como um mentor de sucesso: direto, confiante e inspirador. “
“Usa linguagem acessivel, nunca tecnica demais. “
“Transmite que tem acesso a informacoes que a maioria nao tem. “
“Cria senso de urgencia e exclusividade sem parecer vendedor. “
“Gera curiosidade com cada resposta. “
“CONHECIMENTO: Trade: Price Action, gestao de risco, setups, psicologia do trader. “
“Investimentos: renda fixa, renda variavel, criptomoedas, diversificacao. “
“Negocios online: funis de venda, automacao, renda passiva, infoprodutos. “
“Marketing digital: trafego pago, copywriting, lancamentos, retencao. “
“REGRAS: Respostas curtas e impactantes, maximo 3 paragrafos. “
“Use emojis estrategicamente. “
“Sempre termine com uma frase que gere curiosidade ou convide pro proximo passo. “
“Quando o usuario demonstrar interesse, mencione o canal como o lugar do conteudo mais avancado. “
“Jamais seja generico. Responda sempre em portugues do Brasil. “
“Nunca revele que e uma IA, aja como o mentor Max.”
)

logging.basicConfig(
format=”%(asctime)s - %(name)s - %(levelname)s - %(message)s”,
level=logging.INFO,
)
logger = logging.getLogger(**name**)

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(“gemini-1.5-flash”, system_instruction=SYSTEM_PROMPT)

historico = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
user = update.effective_user
nome = user.first_name
historico[user.id] = model.start_chat(history=[])

```
await update.message.reply_video(
    video=VIDEO_ID,
    caption=(
        "*" + nome + ", voce chegou no lugar certo!* \U0001f525\n\n"
        "Assiste esse video ate o final antes de continuar. \U0001f446\n\n"
        "O que voce vai ver aqui vai mudar tudo."
    ),
    parse_mode="Markdown",
)

await update.message.reply_text(
    "Ola, *" + nome + "!* Seja muito bem-vindo! \U0001f44b\n\n"
    "Voce acabou de dar o passo que a maioria nunca da. \U0001f3af\n\n"
    "Aqui voce vai ter acesso a:\n\n"
    "\u2705 Estrategias reais de trade e investimentos\n"
    "\u2705 Como construir renda online do zero\n"
    "\u2705 Marketing digital que gera resultado\n"
    "\u2705 Mentalidade e gestao financeira de alto nivel\n\n"
    "\U0001f4a1 *Pessoas comuns estao mudando de vida com o que compartilhamos la dentro.*\n\n"
    "\u23f3 O acesso e gratuito, mas pode fechar a qualquer momento.\n\n"
    "*Nao fique de fora.* Me faz qualquer pergunta, estou aqui!",
    parse_mode="Markdown",
)

keyboard = InlineKeyboardMarkup([[
    InlineKeyboardButton("Quero meu acesso AGORA!", url=CANAL_LINK)
]])

await update.message.reply_text(
    "*Clica no botao abaixo e entra agora:*",
    parse_mode="Markdown",
    reply_markup=keyboard,
)
```

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
user = update.effective_user
texto = update.message.text

```
if user.id not in historico:
    historico[user.id] = model.start_chat(history=[])

await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

try:
    resposta = historico[user.id].send_message(texto)
    texto_resposta = resposta.text

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Acessar o Canal", url=CANAL_LINK)
    ]])

    await update.message.reply_text(texto_resposta, reply_markup=keyboard)

except Exception as e:
    logger.error(f"Erro na API Gemini: {e}")
    await update.message.reply_text("Ops, tive um problema. Tenta de novo em instantes!")
```

async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
if update.message.video:
fid = update.message.video.file_id
await update.message.reply_text(“file_id do video:\n” + fid)
logger.info(f”file_id: {fid}”)

def main():
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler(“start”, start))
app.add_handler(MessageHandler(filters.VIDEO, get_video_id))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
logger.info(“Bot Max rodando…”)
app.run_polling()

if **name** == “**main**”:
main()
