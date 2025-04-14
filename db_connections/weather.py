from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import User, Location


async def get_user_by_user_tg_id(
        session: AsyncSession,
        user_tg_id: int,
) -> User | None:
    return await session.scalar(
        select(User)
        .options(joinedload(User.locations))
        .where(User.user_tg_id == user_tg_id)
    )


async def create_user(
        session: AsyncSession,
        user_data: dict[str: str | int],
) -> User:
    user = User(**user_data)
    session.add(user)
    await session.commit()

    return await session.scalar(
        select(User)
        .options(joinedload(User.locations))
        .where(User.user_tg_id == user.user_tg_id)
    )


async def create_location(
        session: AsyncSession,
        user: User,
        location_data: dict[str: str | float],
):
    location: Location | None = await session.scalar(
        select(Location)
        .where(Location.city == location_data['city'])
    )
    if location is None:
        location = Location(**location_data)
        session.add(location)
        await session.flush()

    user.locations.append(location)
    await session.commit()

    return location
