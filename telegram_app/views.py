from telegram import (
    InlineQueryResultArticle, InputTextMessageContent
)
from telegram.error import TelegramError
from telegram.parsemode import ParseMode
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from rest_framework import status

from products.models import Product

from .settings import bot, webhook_url, base_url, markdown_v2
from .messages import *
from .utils.general_utils import (
    get_update_obj, IncrementString
)
from .utils.search_utils import search_products
from .utils.search_utils import ProductMarkup, search_all_categories
from .utils.general_utils import markdown_sanitizer

do_nothing_code = "d8-3;42f"
bad_request = {}


def get_chat_msg_ids(update):
    chat_id = update.effective_chat.id
    msg_id = update.effective_message.message_id
    return chat_id, msg_id


def set_webhook(request):
    set_ = bot.set_webhook(webhook_url)
    if not set_:
        # Todo: Change to Raise Configuration Error
        raise ValueError("Webhook not set")
    return HttpResponse(f"Webhook set to: {base_url}***bot token***/", status=status.HTTP_200_OK)


def efr_loop(update, *args, **kwargs):
    """
    End Failed Request Loop. This decorator catches application errors and returns
    a useful response after a certain number of retries.
    """
    update_id = update.update_id
    max_retries = 3

    def handler(func):
        try:
            return func(update, *args, *kwargs)
        except (TelegramError, Exception):  # Might need to differentiate this error soon.
            if not bad_request or bad_request.get(update_id) is None:
                bad_request[update_id] = 1
            else:
                count = bad_request[update_id]
                if count == max_retries:
                    bad_request.pop(update_id)
                    return error_replier(update)
                bad_request[update_id] += 1
            raise       # Or return 500 server error HTTP response

    return handler


@csrf_exempt
def telegram_view_dispatcher(request):
    update = get_update_obj(request, bot)
    _ = efr_loop

    try:
        # Messages
        if update.message:
            text = update.message.text.encode("utf-8").decode()
            if text == do_nothing_code:
                return HttpResponse(status=status.HTTP_200_OK)
            if text == "/start":
                return _(update)(start)
            # Queries block
            prod_inst = Product.objects.get_obj_or_none(text)
            if prod_inst:   # for automated queries
                return _(update, prod_inst)(return_single_product)
            else:
                # for random queries
                return _(update)(product_not_found)

        # Inline Queries
        elif update.inline_query:
            return _(update)(inline_search)

        # Callback Queries
        elif update.callback_query:
            c_query = update.callback_query
            if c_query.data.startswith("add_to_cart-"):
                return _(update)(product_not_found)
            elif c_query.data.startswith("follow_price-"):
                return _(update)(product_not_found)
            else:
                bot.answer_callback_query(c_query.id, "No Response")
                return HttpResponse(status=status.HTTP_200_OK)
        return _(update)(product_not_found)
    except Exception:
        return _(update)(error_replier)


def error_replier(update):
    chat_id, msg_id = get_chat_msg_ids(update)

    bot.send_message(
        chat_id=chat_id, text=error_replier_message, reply_to_message_id=msg_id,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    return HttpResponse(status=status.HTTP_200_OK)


def start(update):
    chat_id, msg_id = get_chat_msg_ids(update)

    bot.send_message(
        chat_id=chat_id, text=start_message, reply_to_message_id=msg_id,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    return HttpResponse(status=status.HTTP_200_OK)


def return_single_product(update, *args):
    chat_id, msg_id = get_chat_msg_ids(update)
    prod_inst = args[0]
    query = update.message.text
    keyboards = [
        [
            InlineKeyboardButton(
                text="Add To Cart",
                callback_data=f"add_to_cart-{query}"
            ),
            InlineKeyboardButton(
                text="Follow Price",
                callback_data=f"follow_price-{query}"
            )
        ]
    ]

    text = ProductMarkup(prod_inst).message()
    bot.send_message(
        chat_id=chat_id, text=text,
        reply_to_message_id=msg_id,
        reply_markup=InlineKeyboardMarkup(keyboards),
        parse_mode=ParseMode.MARKDOWN_V2
    )
    return HttpResponse(status=status.HTTP_200_OK)


def product_not_found(update):
    chat_id, msg_id = get_chat_msg_ids(update)

    bot.send_message(
        chat_id=chat_id, text=product_not_found_msg,
        reply_to_message_id=msg_id,
        parse_mode=ParseMode.MARKDOWN_V2
    )
    return HttpResponse(status=status.HTTP_200_OK)


def inline_search(update):
    query = update.inline_query.query
    results = list()
    if not query:
        return HttpResponse(status=status.HTTP_200_OK)

    string_id = IncrementString(query)
    search_res = search_products(query)
    if search_res is None:
        results.append(
            InlineQueryResultArticle(
                id="no results",
                title=f"Oops! Seems like we don't have this item '{query}\nClick and we'll notify you when we have it",
                input_message_content=InputTextMessageContent(f"notify_me-{query}"),
            )
        )
    else:
        search_res, suggestions = search_res
        if not suggestions:
            for prod_obj in search_res:
                results.append(
                    InlineQueryResultArticle(
                        id=string_id(),
                        title=prod_obj.full_name,
                        input_message_content=InputTextMessageContent(prod_obj.full_name),
                    )
                )
        else:   # Suggestions
            for prod_obj in search_res:
                results.append(
                    InlineQueryResultArticle(
                        id=string_id(),
                        title=f"{prod_obj.full_name} - Suggestion",
                        input_message_content=InputTextMessageContent(prod_obj.full_name),
                    )
                )

    bot.answer_inline_query(update.inline_query.id, results)
    return HttpResponse(status=status.HTTP_200_OK)