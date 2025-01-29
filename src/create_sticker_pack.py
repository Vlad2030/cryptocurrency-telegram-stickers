import asyncio
import os

import assets
from core.data import Config, Telegram
from core.logging import logger
from core.stickers import sticker_emoji_list, sticker_keywords
from core.telegram import aiogram, bot

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


async def main() -> None:
    bot_data = await bot.get_me()
    channel_data = await bot.get_chat(Telegram.channel_id.to_int())

    default_stickers = [
        aiogram.types.InputSticker(
            sticker=aiogram.types.FSInputFile(
                path=(assets.images_templates_path + sticker),
            ),
            emoji_list=sticker_emoji_list,
            keywords=sticker_keywords,
        )
        for sticker in [
            filename
            for filename in os.listdir(assets.images_templates_path)
            if os.path.isfile(
                os.path.join(assets.images_templates_path, filename)
            )
        ]
    ]
    sticker_pack = await bot.create_new_sticker_set(
        user_id=Telegram.user_id.to_int(),
        name=f"top_cryptocurrencies_by_{bot_data.username}",
        title=f"TOP {Config.top_currency_amount.to_string()} crypto by {channel_data.username}",
        stickers=default_stickers,
        sticker_format="static",
        sticker_type="regular",
    )

    logger.info(f"Sticker pack is created: {sticker_pack}")
    logger.info(
        f"Sticker set link: https://t.me/addstickers/top_cryptocurrencies_by{bot_data.username}",
    )


if __name__ == "__main__":
    loop.run_until_complete(main())
