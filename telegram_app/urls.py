import os
from django.urls import path, include

from .views import telegram_view_dispatcher, set_webhook
from .settings import BOT_TOKEN


urlpatterns = [
    path(f"{BOT_TOKEN}/", telegram_view_dispatcher),
    path(f"{BOT_TOKEN}/set-webhook/", set_webhook)
]

# Set webhook without bot token in url for development and staging
if os.environ.get("DJANGO_SETTINGS_MODULE") != "online_store.settings.production":
    urlpatterns += [
        path("set-webhook/", set_webhook)
    ]
