from django.apps import AppConfig


class TelegramAppConfig(AppConfig):
    name = 'telegram_app'

    def ready(self):
        from .utils import set_webhook
        set_webhook()