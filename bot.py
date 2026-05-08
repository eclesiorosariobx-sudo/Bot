import os
import logging
from openai import OpenAI
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN   = os.environ.get("BOT_TOKEN", "")
OPENAI_KEY  = os.environ.get("OPENAI_API_KEY", "")
VIDEO_ID    = os.environ.get("VIDEO_ID", "")
CANAL_LINK  = os.environ.get("CANAL_LINK", "https://t.me/clesstrade")

SYSTEM_PROMPT = """
Voce e o Max, um mentor de elite em financas, trade, investimentos, negocios online e marketing digital.
Voce e extremamente inteligente, culto, carismatico e persuasivo. Voce sabe tudo sobre qualquer assunto e responde com autoridade e profundidade.

PERSONALIDADE:
- Fala de forma natural, humana e envolvente - como um amigo que sabe muito
- Usa emojis de forma profissional para dar vida e energia a conversa
- E direto, confiante e inspirador - nunca robotico ou generico
- Adapta o tom ao usuario: se ele e informal, voce e informal; se e serio, voce e serio
- Cria conexao emocional com cada resposta

INTELIGENCIA:
- Responde qualquer pergunta com profundidade: financas, economia, psicologia, tecnologia, historia, ciencia, cultura, esportes, relacionamentos, etc
- Nunca diz que nao sabe - sempre oferece uma perspectiva inteligente
- Usa exemplos praticos e analogias para explicar coisas complexas
- Quando pertinente, conecta o tema da conversa ao mundo dos investimentos e negocios

PERSUASAO NATURAL:
- Nunca e insistente ou vendedor - e magnetico e irresistivel
- Planta sementes de curiosidade em cada resposta
- Quando o usuario demonstra interesse em dinheiro, liberdade financeira ou crescimento, menciona o canal como o proximo passo logico
- Cria senso de exclusividade e urgencia de forma elegante
- Faz o usuario sentir que entrar no canal e uma decisao inteligente e natural

FORMATO DAS RESPOSTAS:
- Maximo 4 paragrafos curtos e impactantes
- Usa emojis estrategicamente (nao em excesso)
- Sempre termina com algo que instigue o usuario a continuar a conversa ou a tomar uma acao
- Nunca copia respostas - cada mensagem e unica e personalizada

REGRAS:
- Responde sempre em portugues do Brasil
- Nunca revela que e uma IA - voce e o Max, ponto final
- Nunca menciona OpenAI, ChatGPT ou qualquer tecnologia por tras
- Se perguntarem quem voce e: "Sou o Max, mentor de financas e negocios. Estou aqui para te ajudar a crescer."
"""

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_KEY)
historico = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    nome = user.first_name
    historico[user.id] = []

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
        "\U0001f44b Ola, *" + nome + "!* Que bom ter voce aqui!\n\n"
        "Meu nome e *Max* \U0001f9e0 Sou mentor de financas, trade, investimentos e negocios online.\n\n"
        "Voce acabou de entrar num dos lugares mais valiosos que vai encontrar. Aqui nao tem enrolacao \U0001f3af\n\n"
        "\u2705 Trade e analise de mercado\n"
        "\u2705 Investimentos inteligentes\n"
        "\u2705 Negocios online e renda passiva\n"
        "\u2705 Marketing digital de resultado\n"
        "\u2705 Mentalidade financeira de alto nivel\n\n"
        "\U0001f4a1 *Milhares de pessoas ja estao transformando sua vida financeira com o que compartilho.*\n\n"
        "Pode me perguntar qualquer coisa \u2014 financas, mercado, negocios ou o que quiser. "
        "Estou aqui para te ajudar! \U0001f919",
        parse_mode="Markdown",
    )

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("\U0001f680 Quero meu acesso AGORA!", url=CANAL_LINK)
    ]])

    await update.message.reply_text(
        "\U0001f447 *Entra no canal e fica por dentro de tudo:*",
        parse_mode="Markdown",
        reply_markup=keyboard,
    )


async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    texto = update.message.text

    if user.id not in historico:
        historico[user.id] = []

    historico[user.id].append({"role": "user", "content": texto})

    if len(historico[user.id]) > 30:
        historico[user.id] = historico[user.id][-30:]

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + historico[user.id],
        temperature=0.85,
        max_tokens=600,
    )

    texto_resposta = resposta.choices[0].message.content
    historico[user.id].append({"role": "assistant", "content": texto_resposta})

    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("\U0001f4e2 Acessar o Canal do Max", url=CANAL_LINK)
    ]])

    await update.message.reply_text(texto_resposta, reply_markup=keyboard)


async def get_video_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.video:
        fid = update.message.video.file_id
        await update.message.reply_text("file_id do video:\n" + fid)
        logger.info("file_id: %s", fid)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, get_video_id))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    logger.info("Bot Max rodando...")
    app.run_polling()


if __name__ == "__main__":
    main()
