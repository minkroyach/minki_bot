import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

OWNER_ID = int(os.getenv("OWNER_ID"))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("хелоу!! тут можно оставить в баночке мысль, вопросик или тёплый пук 😌\nотвечаю, как только смочь")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    await context.bot.send_message(chat_id=OWNER_ID, text=f"💌 Новое сообщение от @{user.username or 'анон'}:
{text}")
    await update.message.reply_text("🥺💭 записано в баночку")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) < 2:
        await update.message.reply_text("Используй: /reply <user_id> <текст>")
        return

    user_id = context.args[0]
    text = ' '.join(context.args[1:])
    try:
        await context.bot.send_message(chat_id=int(user_id), text=f"📬 Ответ: {text}")
        await update.message.reply_text("✅ Ответ отправлен")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

def main():
    token = os.getenv("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reply", reply))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()