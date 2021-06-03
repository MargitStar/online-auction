import asyncio
import decimal
import logging
import os
import random

import aiohttp
from user_imitation_tool.cli import parse_arguments
from user_imitation_tool.config import read_config, AppConfig
from user_imitation_tool.utils import ApiClient, get_users

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'DEBUG'))


async def user_flow(current_user, session, api_config):
    offset = 0
    api_client = ApiClient(api_config.api_url, session, current_user.username, current_user.password)
    while True:
        delta_price = random.randint(*api_config.delta_price_range)
        sleep_time = random.randint(*api_config.sleep_time_range)

        response = await api_client.get_english_lots(offset)

        lots = response['results']
        logging.info(f"List of available english lots:\n {lots}")

        offset = random.randint(0, response['count'] - 1)
        random_lot = random.choice(lots)

        offered_price = decimal.Decimal(random_lot['auction']['current_price']) + delta_price
        try:
            offer = await api_client.make_offer_on_english_lot(random_lot['pk'], offered_price)
            logging.info(
                f"Dear, {current_user.username}! {offer} on lot #{random_lot['pk']}. Offered Price is {offered_price}!")
        except aiohttp.ClientResponseError as error:
            if error.status == 400:
                logging.warning(error.message)

        logging.info(f"User: {current_user.username} sleeps...")
        await asyncio.sleep(sleep_time)


async def main():
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        args = parse_arguments()
        config_data = {}
        if args.config_file:
            config_data = read_config(args.config_file)

        config_data = {**config_data, **vars(args)}
        api_config = AppConfig(**config_data)

        users = get_users(api_config.user_file)
        users_tasks = [
            asyncio.create_task(user_flow(current_user, session, api_config))
            for current_user in users
        ]
        await asyncio.wait(users_tasks)
