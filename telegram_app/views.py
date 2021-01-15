from decouple import config
import logging

from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler

from online_store.products.models import Product, Category, search_all_categories
from .searches import ProductMarkup
from .utils import IncrementString

start_message = "Hello, I can help you search and make orders for audio gears in Nigeria.\n\n" \
                "Type the name of an item you want to search for -\n" \
                "e.g Focusrite Scarlett 2i2\n" \
                "We'll check if we have it in stock"


BOT_TOKEN = config("BOT_TOKEN")

updater = Updater(BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update, context):
    print(f"start_update: {update}")
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=start_message
    )


def inline_caps(update, context):
    print(f"inline_update: {update}\n")
    query = update.inline_query.query
    results = list()
    if not query:
        string_id = IncrementString("no_query")
        for prod_obj in Product.objects.all():
            markup = ProductMarkup(prod_obj).message()
            results.append(
                InlineQueryResultArticle(
                    id=string_id(),
                    title=prod_obj.full_name,
                    input_message_content=InputTextMessageContent(markup),
                    parse_mode="MarkdownV2"
                )
            )
    else:
        string_id = IncrementString(query)
        for prod_obj in Product.objects.full_search().results:
            markup = ProductMarkup(prod_obj).message()
            results.append(
                InlineQueryResultArticle(
                    id=string_id(),
                    title=prod_obj.full_name,
                    input_message_content=InputTextMessageContent(markup),
                    parse_mode="MarkdownV2"
                )
            )

    context.bot.answer_inline_query(update.inline_query.id, results)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)


updater.start_polling()









