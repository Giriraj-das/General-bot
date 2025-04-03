from aiogram import types

from db_connections.weather import (
    get_user_by_user_tg_id,
    create_user,
    create_location,
)
from models import db_helper, User, Location


async def get_locations_list(user_tg_id: int) -> list[Location]:
    async for session in db_helper.session_dependency():
        user: User | None = await get_user_by_user_tg_id(
            session=session,
            user_tg_id=user_tg_id,
        )
        return user.locations if user else []


async def create_location_service(
        location_string: str,
        message: types.Message,
):
    city, latitude, longitude = location_string.split('\n')
    location_data = {
        'city': city,
        'latitude': float(latitude),
        'longitude': float(longitude),
    }
    user_data = {
        'user_tg_id': message.from_user.id,
        'first_name': message.from_user.first_name,
        'last_name': message.from_user.last_name,
        'username': message.from_user.username,
    }

    async for session in db_helper.session_dependency():
        user: User | None = await get_user_by_user_tg_id(
            session=session,
            user_tg_id=message.from_user.id,
        )
        if not user:
            user = await create_user(
                session=session,
                user_data=user_data,
            )
        await create_location(
            session=session,
            user=user,
            location_data=location_data,
        )
