import os

import assets
from core.coingecko import CoinGeckoV3Client
from core.data import CoinGecko, Config
from core.logging import logger
from utils import images

cached_logo: dict = {
    # example
    # "name": "str_base64_encoded_image",
}
cached_market: list[dict] = [
    # example
    # {
    # "id": "bitcoin",
    # "symbol": "btc",
    # "name": "Bitcoin",
    # "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1696501400",
    # "current_price": 104625.12,
    # "market_cap": 1381651251183,
    # "market_cap_rank": 1,
    # "fully_diluted_valuation": 1474623675796,
    # "total_volume": 20154184933,
    # "high_24h": 70215,
    # "low_24h": 68060,
    # "price_change_24h": 2126.88,
    # "price_change_percentage_24h": 3.12502,
    # "market_cap_change_24h": 44287678051,
    # "market_cap_change_percentage_24h": 3.31157,
    # "circulating_supply": 19675987,
    # "total_supply": 21000000,
    # "max_supply": 21000000,
    # "ath": 73738,
    # "ath_change_percentage": -4.77063,
    # "ath_date": "2024-03-14T07:10:36.635Z",
    # "atl": 67.81,
    # "atl_change_percentage": 103455.83335,
    # "atl_date": "2013-07-06T00:00:00.000Z",
    # "roi": None,
    # "last_updated": "2024-04-07T16:49:31.736Z",
    # }
]


def _initialize_cache() -> None:
    global cached_logo

    logger.debug("Initializing cache logo..")

    [
        cached_logo.__setitem__(
            filename.split(".png")[0],
            images.to_base64(
                images.get(
                    file_path=(assets.images_cryptocurrencies_path + filename),
                )
            ),
        )
        for filename in os.listdir(
            path=assets.images_cryptocurrencies_path,
        )
        if os.path.isfile(
            os.path.join(
                assets.images_cryptocurrencies_path,
                filename,
            ),
        )
        and filename.endswith(".png")
    ]

    logger.debug("Initialized cache logo..")


async def _initialize_market() -> None:
    global cached_market

    cached_market = []

    logger.debug("Initializing cache market..")

    coingecko_client = CoinGeckoV3Client(api_key=CoinGecko.api_key.to_string())
    markets_request = await coingecko_client.markets(
        vs_currency=Config.currency.to_string(),
    )

    if markets_request.status != 200:
        logger.error("Error to initialize cache market..")

    markets = await markets_request.json()
    await coingecko_client.session.close()

    [cached_market.append(market) for market in markets[0:100]]

    logger.debug("Initialized cache market..")


async def initialize() -> None:
    logger.debug("Initializing..")

    _initialize_cache()
    await _initialize_market()
