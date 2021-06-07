import decimal
import logging
import random

from user_imitation_tool.decorators import handle_bad_request


class LotManager:
    def __init__(self, delta_price_range, api_client, user):
        self.delta_price_range = delta_price_range
        self.api_client = api_client
        self.user = user

    @handle_bad_request(log_label='offering price')
    async def make_offer_on_english_lot(self, lot):
        delta_price = random.randint(*self.delta_price_range)
        offered_price = decimal.Decimal(lot['auction']['current_price']) + delta_price
        offer = await self.api_client.make_offer_on_english_lot(lot['pk'], offered_price)
        logging.info(
            f"Dear, {self.user.username}! "
            f"{offer} on lot #{lot['pk']}. "
            f"Offered Price is {offered_price}!"
        )

    @handle_bad_request(log_label='buying auction')
    async def buy_lot_now(self, lot, request_method):
        lot_pk = lot['pk']
        response = await request_method(lot_pk)
        logging.info(f'{response}! Lot #{lot_pk}')
