from telegram import (
    InlineQueryResultArticle, InputTextMessageContent
)

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from rest_framework import status

from products.models import Product

from .settings import bot, webhook_url
from .messages import *
from .utils.general_utils import (
    get_update_obj, IncrementString
)
from .utils.search_utils import ProductMarkup, search_all_categories


def set_webhook(request):
    set_ = bot.set_webhook(webhook_url)
    print(f"Webhook url: {webhook_url}")
    if not set_:
        # Todo: Change to Raise Configuration Error
        raise ValueError("Webhook not set")
    return HttpResponse("Webhook Set", status=status.HTTP_200_OK)


@csrf_exempt
def telegram_view_dispatcher(request):
    update = get_update_obj(request, bot)
    if update.message:
        text = update.message.text.encode("utf-8").decode()
        if text == "/start":
            return start(update)
    elif update.inline_query:
        return inline_search(update)


def start(update):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    bot.send_message(
        chat_id=chat_id, text=start_message, reply_to_message_id=msg_id,
        parse_mode="MarkdownV2"
    )
    return HttpResponse(status=status.HTTP_200_OK)


def inline_search(update):
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

    bot.answer_inline_query(update.inline_query.id, results)