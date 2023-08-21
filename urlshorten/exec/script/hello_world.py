import asyncio

import structlog

logger = structlog.get_logger("main")


async def process() -> None:
    logger.info("hello world")

    await asyncio.sleep(43200)
