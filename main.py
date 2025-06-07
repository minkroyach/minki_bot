import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
BOT_OWNER_ID = 1030243433

WELCOME_MESSAGE = (
    "хелоу!! тут можно оставить в баночке мысль, вопросик или тёплый пук 😌\n"
    "отвечаю, как только смочь"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MESSAGE)

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await context.bot.send_message(
            chat_id=BOT_OWNER_ID,
            text=f"💌 Новое сообщение:
{update.message.text}"
        )
        await update.message.reply_text("отправлено в баночку 💌")

app = ApplicationBuilder().token(os.getenv("API_TOKEN")).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_message))

if __name__ == "__main__":
    app.run_polling()
