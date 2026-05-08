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

BOT_TOKEN  = os.environ.get("BOT_TOKEN", "")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
VIDEO_ID   = os.environ.get("VIDEO_ID", "")
CANAL_LINK = os.environ.get("CANAL_LINK", "https://t.me/+SEU_LINK")

SYSTEM_PROMPT = (
    "Voce e um especialista de alto nivel em trade, financas, investimentos, negocios online e marketing digital. "
    "Seu nome e Max, um mentor direto, inteligente e extremamente persuasivo. "
    "Fala como um mentor de sucesso: direto, confiante e inspirador. "
    "Usa linguagem acessivel, nunca tecnica demais. "
    "Respostas curtas e impactantes, maximo 3 paragrafos. "
    "Use emojis estrategicamente. "
    "Sempre termine com uma frase que gere curiosidade ou convide pro proximo passo. "
    "Jamais seja generico. Responda sempre em portugues do Brasil. "
    "Nunca revele que e uma IA, aja como o mentor Max."
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.WARNING,
)
logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    nome = user.first_name

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


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    texto = update.message.text

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        prompt = SYSTEM_PROMPT + "\n\nUsuario disse: " + texto
        resposta = model.generate_content(prompt)
        texto_resposta = resposta.text
    except Exception as e:
        logger.error("Erro ao gerar resposta: %s", str(e))
        texto_resposta = "Desculpa, tive um problema ao processar sua mensagem. Tenta de novo!"

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Acessar o Canal", url=CANAL_LINK)
    ]])

    await update.message.reply_text(texto_resposta, reply_markup=keyboard)


async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        fid = update.message.video.file_id
        await update.message.reply_text("file_id do video:\n" + fid)
        logger.info("file_id: %s", fid)


def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN nao configurado!")
        return

    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, get_video_id))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    logger.info("Bot Max rodando...")
    app.run_polling()


if __name__ == "__main__":
    main()
