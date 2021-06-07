import json
import logging

from pydantic import BaseModel, Field
from json import JSONDecodeError


class ReadConfigError(Exception):
    pass


class AppConfig(BaseModel):
    url: str
    user_file: str
    sleep_time_range: tuple[(int, int)] = Field(default=tuple((1, 5)))
    delta_price_range: tuple[(int, int)] = Field(default=tuple((1, 20)))


def read_config(path):
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except (JSONDecodeError, TypeError, OSError) as error:
        raise ReadConfigError(f'Cannot load config. error: {error}')
