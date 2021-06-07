import logging
import sys
from functools import wraps

import aiohttp
from retry.api import retry_call


def handle_refresh(method):
    @wraps(method)
    async def wrapper(self, *args, **kwargs):
        try:
            return await method(self, *args, **kwargs)
        except aiohttp.ClientResponseError as error:
            if error.status != 401:
                raise
            logging.debug('Access token expired. Getting new access token')
            await self.refresh()
            return await retry_call(method, fargs=(self, *args), fkwargs=kwargs, tries=5, backoff=2, jitter=(0, 1))

    return wrapper


def handle_exception_main(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as error:
            logging.error(f"App error: {error}")
            sys.exit(1)

    return wrapper
