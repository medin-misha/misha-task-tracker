import aiohttp
from aiogram.fsm.context import FSMContext
from datetime import datetime
from typing import Dict
from settings import config
from .auth import base_encode


async def create_task(state: FSMContext, user_name: str, user_id: int) -> dict | None:
    async with aiohttp.ClientSession() as session:
        auth_base64 = base_encode(user_name=user_name, user_id=user_id)
        headers: Dict[str, str] = {"Authorization": f"Basic {auth_base64}"}
        state_data: dict = await state.get_data()
        data: Dict[str, dict] = {
            "replay_data": {
                "replay_data": 0,
                "date": state_data.get("date"),
                "replay_mode": state_data.get("replay_mode"),
                "time": datetime.now().strftime("%H:%M:%S.%f"),
            },
            "task_data": {
                "name": state_data.get("name"),
                "description": state_data.get("description"),
                "is_complete": False,
            },
        }
        async with session.post(
            url=config.api_address + "tasks/", json=data, headers=headers
        ) as response:
            return (await response.json(), response.status, response.text)


async def tasks(user_name: str, user_id: int, how_many_days: int = 1):
    async with aiohttp.ClientSession() as session:
        auth_base64 = base_encode(user_name=user_name, user_id=user_id)
        headers: Dict[str, str] = {"Authorization": f"Basic {auth_base64}"}
        async with session.get(
            url=config.api_address + f"tasks/get/{how_many_days}/calendar",
            headers=headers,
        ) as response:
            return await response.json()


async def delete_task(id: str, user_name: str, user_id: str) -> bool:
    async with aiohttp.ClientSession() as session:
        auth_base64 = base_encode(user_name=user_name, user_id=user_id)
        headers: Dict[str, str] = {"Authorization": f"Basic {auth_base64}"}
        async with session.delete(
            url=config.api_address + f"tasks/{id}", headers=headers
        ) as response:
            return False if response.status != 204 else True


async def complete_task(id: str, user_name: str, user_id: str) -> bool:
    async with aiohttp.ClientSession() as session:
        auth_base64 = base_encode(user_name=user_name, user_id=user_id)
        headers: Dict[str, str] = {"Authorization": f"Basic {auth_base64}"}
        async with session.get(
            config.api_address + f"tasks/complete/{id}", headers=headers
        ) as response:
            return False if response.status != 204 else True
