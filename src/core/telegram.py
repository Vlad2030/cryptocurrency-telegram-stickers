import aiogram
import aiogram.client.default
from aiogram.utils import markdown as md

from core.data import Telegram

bot = aiogram.Bot(
    token=Telegram.bot_token.to_string(),
    default=aiogram.client.default.DefaultBotProperties(
        parse_mode=aiogram.enums.ParseMode.HTML,
    ),
)
