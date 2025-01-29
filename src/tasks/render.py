import datetime
import multiprocessing

import core.cache
import core.render
from core.logging import logger


def render_stickers_task() -> None:
    logger.info("Rendering stickers..")

    timestamp = datetime.datetime.now(datetime.UTC).replace(second=0)

    iter_data = [
        {
            "count": count,
            "symbol": market["symbol"],
            "name": market["name"],
            "image": market["image"],
            "price": market["current_price"],
            "market_cap": market["market_cap"],
            "price_change_percent": market["price_change_percentage_24h"],
            "timestamp": timestamp,
            "extra_text": "By @chad_trade",
            "round_logo": True,
            "mode": "white" if 21 > timestamp.hour > 9 else "black",
        }
        for count, market in enumerate(core.cache.cached_market[0:100])
    ]

    with multiprocessing.Pool(processes=4) as pool:
        pool.map(func=core.render.process_render, iterable=iter_data)
