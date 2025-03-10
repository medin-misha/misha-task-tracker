import aiohttp
from typing import Dict
from settings import config
from utils.encode import base_encode


async def registration(user_name: str, user_id: int) -> int:
    async with aiohttp.ClientSession() as session:
        data: Dict[str, str] = {
            "user_name": user_name,
            "chat_id": str(user_id),
        }
        async with session.post(
            url=config.api_address + "auth/registration", json=data
        ) as response:
            return response.status


async def login(user_name: str, user_id: int) -> int:
    async with aiohttp.ClientSession() as session:
        auth_base64 = base_encode(user_name=user_name, user_id=user_id)
        headers: Dict[str, str] = {"Authorization": f"Basic {auth_base64}"}
        async with session.get(
            url=config.api_address + "auth/login", headers=headers
        ) as response:
            return response.status
