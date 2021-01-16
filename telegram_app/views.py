import telegram
import json

from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse

from rest_framework import status

from .settings import bot, webhook_url
from .messages import *


def set_webhook(request):
    set_ = bot.set_webhook(webhook_url)
    print(f"Webhook url: {webhook_url}")
    if not set_:
        # Todo: Change to Raise Configuration Error
        raise ValueError("Webhook not set")
    return HttpResponse("Webhook Set", status=status.HTTP_200_OK)


@csrf_exempt
def telegram_view_dispatcher(request):
    json_body = json.loads(request.body)
    print(f"update: {json_body}")
    update = telegram.Update.de_json(json_body, bot)

    text = update.message.text.encode("utf-8").decode()

    if text == "/start":
        return start(update)


def start(update):
    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    bot.send_message(
        chat_id=chat_id, text=start_message, reply_to_message_id=msg_id,
        parse_mode="MarkdownV2"
    )
    return HttpResponse(status=status.HTTP_200_OK)