from telegram import Update
from telegram.ext import ContextTypes

from extra.config import url
import requests


async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = requests.get(url)
    joke = response.json()
    await update.message.reply_text(f"{joke['setup']}\n"
                                    f"{joke['punchline']}")
