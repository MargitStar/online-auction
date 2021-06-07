import asyncio
import decimal
import logging
import os
import random

import aiohttp
from retry.api import retry

from .cli import parse_arguments
from .config import read_config, AppConfig
from .decorators import handle_exception_main
from .utils import ApiClient, get_users

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'DEBUG'))


async def user_iteration(current_user, api_config, api_client, offset):
    delta_price = random.randint(*api_config.delta_price_range)
    try:
        response = await api_client.get_english_lots(offset)

        lots = response['results']
        if not lots:
            logging.info('Lots are empty')
            return offset
        logging.info(f"List of available english lots:\n {lots}")

        offset = random.randint(0, response['count'] - 1)
        random_lot = random.choice(lots)

        offered_price = decimal.Decimal(random_lot['auction']['current_price']) + delta_price
        try:
            offer = await api_client.make_offer_on_english_lot(random_lot['pk'], offered_price)
            logging.info(
                f"Dear, {current_user.username}! "
                f"{offer} on lot #{random_lot['pk']}. "
                f"Offered Price is {offered_price}!"
            )
        except aiohttp.ClientResponseError as error:
            if error.status != 400:
                raise
            logging.warning(error.message)

        return offset
    except aiohttp.ClientConnectorError:
        logging.error("Can't connect server!")
        return offset


async def user_flow(current_user, session, api_config):
    api_client = ApiClient(api_config.url, session, current_user.username, current_user.password)
    offset = 0
    while True:
        offset = await user_iteration(current_user, api_config, api_client, offset)

        sleep_time = random.randint(*api_config.sleep_time_range)
        logging.info(f"User: {current_user.username} sleeps...")
        await asyncio.sleep(sleep_time)


@handle_exception_main
async def main():
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        args = parse_arguments()

        config_data = read_config(args.config_file) if args.config_file else {}
        config_data = {
            **config_data,
            **{k: v for k, v in vars(args).items() if v is not None},
        }
        api_config = AppConfig(**config_data)

        users = get_users(api_config.user_file)
        users_tasks = [
            asyncio.create_task(user_flow(current_user, session, api_config))
            for current_user in users
        ]
        try:
            await asyncio.wait(users_tasks)
        except aiohttp.ServerDisconnectedError as error:
            logging.error(f"Can't connect server, error={error}")
