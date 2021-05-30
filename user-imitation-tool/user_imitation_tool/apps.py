import asyncio
import decimal
import logging
import os
import random

import aiohttp
from user_imitation_tool.utils import ApiClient, get_users

SLEEPING_TIME = 20
API_URL = 'http://127.0.0.1:8000'
USERS_INFO = 'users.csv'

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'DEBUG'))


async def main():
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        offset = 0
        current_user = get_users(USERS_INFO)[0]
        api_client = ApiClient(API_URL, session, current_user.username, current_user.password)
        while True:
            response = await api_client.get_english_lots(offset)

            logging.info(f"List of available english lots:\n {response}")

            offset = random.randint(0, response['count'] - 1)
            random_lot = random.choice(response['results'])

            delta_price = random.randint(1, 20)
            offered_price = decimal.Decimal(random_lot['auction']['current_price']) + delta_price
            offer = await api_client.make_offer_on_english_lot(random_lot['pk'], offered_price)
            logging.info(
                f"Dear, {current_user.username}! {offer} on lot #{random_lot['pk']}. Offered Price is {offered_price}!")

            logging.info(f"User: {current_user.username} sleeps...")
            await asyncio.sleep(SLEEPING_TIME)
