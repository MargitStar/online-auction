import csv
import logging
from typing import NamedTuple

import aiohttp

from .decorators import handle_refresh


class User(NamedTuple):
    username: str
    password: str


def get_users(path):
    with open(path) as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=['username', 'password'], delimiter=',')
        return [User(**row) for row in csv_reader]


class ApiClient:
    def __init__(self, url, session, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.session = session
        self.access_token = None
        self.refresh_token = None

    @property
    def auth_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    async def authenticate_user(self):
        async with self.session.post(f'{self.url}/jwt/token/',
                                     json={'username': self.username, 'password': self.password}) as response:
            tokens = await response.json()
            self.access_token = tokens['access']
            self.refresh_token = tokens['refresh']

    async def refresh(self):
        try:
            async with self.session.post(f'{self.url}/jwt/token/refresh/',
                                         json={'refresh': self.refresh_token}) as response:
                self.access_token = (await response.json())['access']
        except aiohttp.ClientResponseError:
            logging.debug('Refresh expired. Getting new token pair')
            await self.authenticate_user()

    @handle_refresh
    async def get_english_lots(self, offset):
        async with self.session.get(
                f"{self.url}/lot/",
                headers=self.auth_headers,
                params={'auction__content_type__model': 'english', 'auction__status': '2', 'offset': offset},
                raise_for_status=True) as response:
            return await response.json()

    @handle_refresh
    async def make_offer_on_english_lot(self, pk, offered_price):
        async with self.session.post(f"{self.url}/lot/{pk}/make_offer/", json={'price': str(offered_price)},
                                     headers=self.auth_headers) as response:
            return await response.json()
