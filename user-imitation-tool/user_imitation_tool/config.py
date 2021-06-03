import json

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    api_url: str
    user_file: str
    sleep_time_range: tuple[(int, int)] = Field(default=tuple((1, 5)))
    delta_price_range: tuple[(int, int)] = Field(default=tuple((1, 20)))


def read_config(path):
    with open(path, 'r') as file:
        return json.load(file)
