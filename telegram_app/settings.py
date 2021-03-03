import os
from decouple import config

import telegram

BOT_TOKEN = config("BOT_TOKEN")

# Todo: This hook doesn't make app pluggable, find another way.
# Settings for development and staging/production
if os.environ.get("DJANGO_SETTINGS_MODULE") == "online_store.settings.development" and \
        os.environ.get('GITHUB_WORKFLOW') is None:
    base_url = config('NGROK_BASE_URL')
    webhook_url = f"{base_url}{config('BOT_TOKEN')}/"
else:
    base_url = config('BASE_URL')
    webhook_url = f"{base_url}{config('BOT_TOKEN')}/"


bot = telegram.Bot(token=BOT_TOKEN)

# Parse Modes
markdown_v2, html_pm, markdown = "MarkdownV2", "HTML", "Markdown"