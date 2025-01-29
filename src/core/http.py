import asyncio

import aiohttp
import orjson


class BaseClient:
    def __init__(
        self,
        base_url: str,
        headers: dict | None = None,
        timeout: float = 5.00,
        proxy: str | None = None,
    ) -> None:
        self.base_url = base_url
        self.headers = headers
        self.proxy = proxy
        self.timeout = aiohttp.ClientTimeout(
            sock_connect=timeout,
            sock_read=timeout,
        )
        self.session = aiohttp.ClientSession(
            base_url=self.base_url,
            headers=self.headers,
            timeout=self.timeout,
            json_serialize=(lambda x: orjson.dumps(x).decode()),
            loop=asyncio.get_event_loop(),
        )

    async def request(
        self,
        method: str,
        endpoint: str,
        headers: dict | None = None,
        params: dict | None = None,
        json: dict | None = None,
    ) -> aiohttp.ClientResponse | None:
        try:
            response: aiohttp.ClientResponse = await self.session.request(
                method=method,
                url=endpoint,
                headers=headers,
                params=params,
                json=json,
                proxy=self.proxy,
            )

        except aiohttp.ServerTimeoutError:
            return None

        return response
