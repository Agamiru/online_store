from decouple import config

import telegram

BOT_TOKEN = config("BOT_TOKEN")
webhook_url = f"{config('BASE_URL')}/{config('BOT_TOKEN')}"


bot = telegram.Bot(token=BOT_TOKEN)