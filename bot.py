import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Настройки
OWNER_ID = 1030243433
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Жёсткая проверка токена
if not BOT_TOKEN:
    logging.critical("❌ CRITICAL: BOT_TOKEN не найден в переменных окружения!")
    # Попробуем прочитать из файла (для отладки)
    try:
        with open('token.txt') as f:
            BOT_TOKEN = f.read().strip()
            logging.warning("⚠️ Используется токен из файла token.txt")
    except:
        logging.critical("🚨 Файл token.txt также отсутствует!")
        exit(1)

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
