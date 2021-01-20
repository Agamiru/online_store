from django.urls import path, include

from .views import telegram_view_dispatcher, set_webhook
from .settings import BOT_TOKEN


urlpatterns = [
    path(f"{BOT_TOKEN}/", telegram_view_dispatcher),
    path(f"{BOT_TOKEN}/set-webhook/", set_webhook)
]