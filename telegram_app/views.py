import telegram
import json

from django.http import HttpResponse

from rest_framework import status

from .settings import bot
from .messages import *


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

    bot.sendMessage(
        chat_id=chat_id, text=start_message, reply_to_message_id=msg_id
    )
    return HttpResponse(status=status.HTTP_200_OK)