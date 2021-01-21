import os
from decouple import config

import telegram

BOT_TOKEN = config("BOT_TOKEN")
if os.environ.get("DJANGO_SETTINGS_MODULE") == "online_store.settings.development":
    webhook_url = f"{config('NGROK_BASE_URL')}{config('BOT_TOKEN')}/"
else:
    webhook_url = f"{config('BASE_URL')}{config('BOT_TOKEN')}/"


bot = telegram.Bot(token=BOT_TOKEN)
