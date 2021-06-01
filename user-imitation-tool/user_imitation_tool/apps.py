import asyncio
import decimal
import logging
import os
import random

import aiohttp
from user_imitation_tool.utils import ApiClient, get_users

API_URL = 'http://127.0.0.1:8000'
USERS_INFO = 'users.csv'

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'DEBUG'))


async def user_flow(current_user, session):
    offset = 0
    api_client = ApiClient(API_URL, session, current_user.username, current_user.password)
    while True:
        response = await api_client.get_english_lots(offset)

        logging.info(f"List of available english lots:\n {response}")

        offset = random.randint(0, response['count'] - 1)
        random_lot = random.choice(response['results'])

        delta_price = random.randint(1, 20)
        offered_price = decimal.Decimal(random_lot['auction']['current_price']) + delta_price
        try:
            offer = await api_client.make_offer_on_english_lot(random_lot['pk'], offered_price)
            logging.info(
                f"Dear, {current_user.username}! {offer} on lot #{random_lot['pk']}. Offered Price is {offered_price}!")
        except aiohttp.ClientResponseError as error:
            if error.status == 400:
                logging.warning(error.message)

        logging.info(f"User: {current_user.username} sleeps...")
        await asyncio.sleep(random.randint(1, 5))


async def main():
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        users = get_users(USERS_INFO)
        users_tasks = [asyncio.create_task(user_flow(current_user, session)) for current_user in users]
        await asyncio.wait(users_tasks)
