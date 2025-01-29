import asyncio
import os

import assets
from core.data import Config, Telegram
from core.logging import logger
from core.stickers import sticker_emoji_list, sticker_keywords
from core.telegram import aiogram, bot


async def delete_stickers_in_sticker_set_task() -> None:
    logger.info("Deleting stickers from sticker set..")

    bot_data = await bot.get_me()

    sticker_set = await bot.get_sticker_set(
        name=f"top_cryptocurrencies_by_{bot_data.username}",
    )

    logger.info(f"Found {len(sticker_set.stickers)} stickers in sticker set")

    for sticker in sticker_set.stickers:
        await asyncio.create_task(
            coro=bot.delete_sticker_from_set(sticker.file_id),
        )
        # await bot.delete_sticker_from_set(sticker.file_id)
        logger.info(f"Sticker {sticker.file_id} deleted")

    logger.info("Stickers from sticker set deleted")


async def add_stickers_in_sticker_set_task() -> None:
    logger.info("Adding stickers to sticker set..")

    stickers = [
        aiogram.types.InputSticker(
            sticker=aiogram.types.FSInputFile(
                path=(assets.images_stickers_path + sticker),
            ),
            format="static",
            emoji_list=sticker_emoji_list,
            keywords=sticker_keywords,
        )
        for sticker in [
            filename
            for filename in os.listdir(assets.images_stickers_path)
            if os.path.isfile(
                os.path.join(assets.images_stickers_path, filename)
            )
        ]
    ]

    logger.info(f"Loaded {len(stickers)} stickers")

    bot_data = await bot.get_me()

    for count, sticker in enumerate(stickers):
        await asyncio.create_task(
            coro=(
                bot.add_sticker_to_set(
                    user_id=Telegram.user_id.to_int(),
                    name=f"top_cryptocurrencies_by_{bot_data.username}",
                    sticker=sticker,
                )
            ),
        )
        logger.info(f"Sticker {count} added")

    logger.info("Stickers to sticker set added")
