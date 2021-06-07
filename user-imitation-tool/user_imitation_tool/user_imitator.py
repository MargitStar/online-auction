import asyncio
import logging
import random

import aiohttp

from user_imitation_tool.utils import ApiClient
from user_imitation_tool.lot_retriever import LotRetriever
from user_imitation_tool.lot_manager import LotManager


class UserImitator:
    def __init__(self, user, app_config, session):
        self.user = user
        self.app_config = app_config
        self.api_client = ApiClient(app_config.url, session, user.username, user.password)
        self.lot_retriever = LotRetriever(self.api_client, user)
        self.lot_manager = LotManager(app_config.delta_price_range, self.api_client, user)

    async def start_imitation(self):
        while True:
            try:
                await self.perform_iteration()
            except aiohttp.ClientConnectorError:
                logging.error("Can't connect to server!")

            sleep_time = random.randint(*self.app_config.sleep_time_range)
            logging.info(f"User: {self.user.username} sleeps...")
            await asyncio.sleep(sleep_time)

    async def perform_iteration(self):
        choice = random.randint(1, 2)
        lot, lot_type = await self.lot_retriever.get_random_lot()
        if not lot or not lot_type:
            return

        if lot_type == 'english':
            if choice == 1:
                await self.lot_manager.make_offer_on_english_lot(lot)

            elif choice == 2:
                await self.lot_manager.buy_lot_now(lot, self.api_client.buy_it_now_english)
        elif lot_type == 'dutch':
            if choice == 1:
                await self.lot_manager.buy_lot_now(lot, self.api_client.buy_it_now_dutch)
