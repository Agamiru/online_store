from django.apps import AppConfig


class TelegramAppConfig(AppConfig):
    name = 'telegram_app'

    def ready(self):
        from .settings import bot, webhook_url
        set_ = bot.set_webhook(webhook_url)
        if not set_:
            raise ValueError("Webhook not set")