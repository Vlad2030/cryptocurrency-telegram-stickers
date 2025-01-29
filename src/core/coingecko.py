import aiohttp

from core.http import BaseClient


class CoinGeckoV3Client(BaseClient):
    def __init__(
        self,
        api_key: str,
        proxy: str | None = None,
    ) -> None:
        self.api_key = api_key
        self.base_url = "https://api.coingecko.com/"
        self.headers = {"x-cg-demo-api-key": self.api_key}
        self.timeout = 15
        self.proxy = None

        super().__init__(
            self.base_url,
            self.headers,
            self.timeout,
            self.proxy,
        )

    async def ping(self) -> bool:
        response = await self.request(method="GET", endpoint="/api/v3/ping")

        return True if response.status == 200 else False

    async def markets(
        self,
        vs_currency: str = "usd",
        ids: list[str] | None = None,
        category: str | None = None,
        order: str | None = None,
        per_page: int = 250,
        page: int = 1,
        sparkline: bool = False,
        price_change_percentage: str | None = None,
        locale: str = "en",
        precision: str | None = None,
    ) -> aiohttp.ClientResponse | None:
        params: dict = {
            "vs_currency": vs_currency,
            "per_page": per_page,
            "page": page,
            "sparkline": str(sparkline),
            "locale": locale,
        }

        if ids is not None:
            ids = ",".join(ids)
            params["ids"] = ids

        if category is not None:
            params["category"] = category

        if order is not None:
            params["order"] = order

        if price_change_percentage is not None:
            params["price_change_percentage"] = price_change_percentage

        if precision is not None:
            params["precision"] = precision

        response = await self.request(
            method="GET",
            endpoint="/api/v3/coins/markets/",
            params=params,
        )

        return response
