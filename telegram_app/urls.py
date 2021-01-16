from django.urls import path, include

from .views import telegram_view_dispatcher
from .settings import BOT_TOKEN


urlpatterns = [
    path(f"{BOT_TOKEN}/", telegram_view_dispatcher)
]