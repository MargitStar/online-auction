import asyncio
import logging
import os

import aiohttp

from user_imitation_tool.cli import parse_arguments
from user_imitation_tool.config import read_config, AppConfig
from user_imitation_tool.decorators import handle_exception_main
from user_imitation_tool.user_imitator import UserImitator
from user_imitation_tool.utils import get_users

logging.basicConfig(level=os.environ.get('LOG_LEVEL', 'DEBUG'))

@handle_exception_main
async def main():
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        args = parse_arguments()

        config_data = read_config(args.config_file) if args.config_file else {}
        config_data = {
            **config_data,
            **{k: v for k, v in vars(args).items() if v is not None},
        }
        app_config = AppConfig(**config_data)

        users = get_users(app_config.user_file)
        user_imitators = [UserImitator(user, app_config, session) for user in users]
        users_tasks = [
            asyncio.create_task(user_imitator.start_imitation())
            for user_imitator in user_imitators
        ]
        try:
            await asyncio.wait(users_tasks)
        except aiohttp.ServerDisconnectedError as error:
            logging.error(f"Can't connect server, error={error}")
