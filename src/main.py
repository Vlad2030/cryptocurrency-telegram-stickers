import asyncio
import os
import time

import aiocron

from core import __VERSION__, cache, coingecko, data, telegram
from core.logging import logger
from tasks import cache as tcache
from tasks import render, telegram
from utils import crontab, tasks

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@aiocron.crontab(spec="*/60 * * * *", loop=loop)
@tasks.log
async def update_cache_task() -> None:
    await tcache.update_cache_task()


@aiocron.crontab(
    spec=crontab.generate_expression(
        interval_seconds=data.Config.telegram_stickers_update_interval.to_int(),
    ),
    loop=loop,
)
@tasks.log
async def update_stickers_task() -> None:
    await cache._initialize_market()
    render.render_stickers_task()
    await telegram.delete_stickers_in_sticker_set_task()
    await telegram.add_stickers_in_sticker_set_task()


async def main() -> None:
    logger.info("Created by lalka2003")
    logger.info(f"Version: {__VERSION__}")

    data.Config.__log_repr__(logger)
    data.CoinGecko.__log_repr__(logger)
    data.Telegram.__log_repr__(logger)

    logger.info("Checking GC connection..")

    coingecko_client = coingecko.CoinGeckoV3Client(
        api_key=data.CoinGecko.api_key.to_string(),
    )

    coingecko_connected = await coingecko_client.ping()

    if not coingecko_connected:
        await coingecko_client.session.close()
        logger.warning("GC ping status bad")
        return exit(1)

    logger.info("Checking GC api key..")

    test_request = await coingecko_client.markets()

    if test_request.status == 429:
        await coingecko_client.session.close()
        logger.warning("GC api key is bad")
        return exit(1)

    await coingecko_client.session.close()

    logger.info("Caching logo's..")

    await cache.initialize()

    telegram_bot = await telegram.bot.get_me()

    logger.info(f"Telegram bot: @{telegram_bot.username}")

    telegram_sticker_set = await telegram.bot.get_sticker_set(
        name=f"top_cryptocurrencies_by_{telegram_bot.username}",
    )

    logger.info(f"Telegram sticker set: @{telegram_sticker_set.name}")

    telegram_channel = await telegram.bot.get_chat(
        chat_id=data.Telegram.channel_id.to_int(),
    )
    logger.info(f"Telegram channel: @{telegram_channel.username}")

    logger.info("Sticker set auto update started")

    while True:
        await asyncio.sleep(1.00)

    await telegram.bot.session.close()


if __name__ == "__main__":
    loop.run_until_complete(main())
