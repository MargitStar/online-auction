import logging
import random


class LotRetriever:
    def __init__(self, api_client, user):
        self.offset = 0
        self.api_client = api_client
        self.user = user

    async def get_random_lot(self):
        lots, response = await self.get_lots()
        if not lots or not response:
            return None, None
        self.offset = random.randint(0, response['count'] - 1)
        random_lot = random.choice(lots)

        logging.info(f"Your lot:\n {random_lot}")
        lot_type = random_lot['auction']['auction_type']['lot_type']
        return random_lot, lot_type

    async def get_lots(self):
        response = await self.api_client.get_opened_lots(self.offset)

        lots = response['results']
        if not lots:
            logging.info('Lots are empty!')
            return None, None
        logging.info(f"List of available lots:\n {lots}")
        return lots, response
