import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Настройки
OWNER_ID = 1030243433  # Жёстко прописываем ваш ID
BOT_TOKEN = os.getenv("BOT_TOKEN", "8043165621:AAEnOIxob-8xXkUZNKqJdFbqBEozjtFyMb4")  # Токен по умолчанию

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "хелоу!! тут можно оставить в баночке мысль, вопросик или тёплый пук 😌\n"
        "отвечаю, как только смочь"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка обычных сообщений"""
    user = update.effective_user
    text = update.message.text
    
    # Формируем сообщение для владельца
    owner_message = (
        f"💌 Новое сообщение от @{user.username or 'анон'} (ID: {user.id}):\n\n"
        f"{text}"
    )
    
    try:
        await context.bot.send_message(chat_id=OWNER_ID, text=owner_message)
        await update.message.reply_text("🥺💭 записано в баночку")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /reply для ответов"""
    if update.effective_user.id != OWNER_ID:
        return  # Только владелец может отвечать

    if len(context.args) < 2:
        await update.message.reply_text("ℹ️ Используй: /reply <user_id> <текст>")
        return

    user_id = context.args[0]
    reply_text = ' '.join(context.args[1:])
    
    try:
        await context.bot.send_message(
            chat_id=int(user_id),
            text=f"📬 Ответ от админа:\n\n{reply_text}"
        )
        await update.message.reply_text("✅ Ответ успешно отправлен")
    except Exception as e:
        error_message = f"⚠️ Не удалось отправить ответ: {str(e)}"
        await update.message.reply_text(error_message)
        logger.error(error_message)

def main():
    """Запуск бота"""
    if not BOT_TOKEN:
        logger.critical("❌ BOT_TOKEN не установлен!")
        return
        
    logger.info(f"🚀 Бот запускается для владельца: {OWNER_ID}")
    
    try:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("reply", reply))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.run_polling()
    except Exception as e:
        logger.critical(f"Критическая ошибка: {e}")

if __name__ == "__main__":
    main()
