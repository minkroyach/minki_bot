from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")  # Токен из переменных окружения Railway
ADMIN_ID = 1030243433  # Ваш ID (указан в задании)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "хелоу!! тут можно оставить в баночке мысль, вопросик или тёплый пук 😌\n"
        "отвечаю, как только смочь"
    )

def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id == ADMIN_ID and text.startswith("/reply"):
        # Ответ админа (формат: /reply USER_ID текст)
        try:
            _, target_user_id, reply_text = text.split(" ", 2)
            context.bot.send_message(chat_id=target_user_id, text=f"💌 Ответ: {reply_text}")
            update.message.reply_text("✅ Ответ отправлен!")
        except:
            update.message.reply_text("❌ Ошибка. Используйте: /reply USER_ID ТЕКСТ")
    else:
        # Пересылка сообщения админу
        context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"📥 Новое сообщение от {user_id}:\n\n{text}"
        )
        update.message.reply_text("🍪 Ваше сообщение добавлено в баночку!")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()