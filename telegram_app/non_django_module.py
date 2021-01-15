from decouple import config
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

BOT_TOKEN = config("BOT_TOKEN")

updater = Updater(BOT_TOKEN, use_context=True)
PORT = config("PORT", cast=int())

updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=f"telegram/{BOT_TOKEN}/")

updater.bot.set_webhook(f"https://sabigear-staging.herokuapp.com/telegram/{BOT_TOKEN}/")
dispatcher = updater.dispatcher

start_message = "Hello, I can help you search and make orders for audio gears in Nigeria.\n\n" \
                "Type the name of an item you want to search for -\n" \
                "e.g Focusrite Scarlett 2i2\n" \
                "We'll check if we have it in stock"


def start(update, context):
    print(f"start_update: {update}")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_message
    )


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


updater.idle()