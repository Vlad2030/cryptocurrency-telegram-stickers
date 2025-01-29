import core.cache


async def update_cache_task() -> None:
    await core.cache.initialize()
