from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import User, Location


async def get_locations_by_user_tg_id(
        session: AsyncSession,
        user_tg_id: int,
) -> list[Location]:
    stmt = (
        select(User)
        .where(User.user_tg_id == user_tg_id)
        .options(joinedload(User.locations))
    )
    user = await session.scalar(stmt)

    return user.locations if user else []


# async def create_user(session: AsyncSession, user_data: dict) -> User:
#     user = User(**user_data)
#     session.add(user)
#     await session.commit()
#     return user
#
#
# async def get_users(session: AsyncSession) -> list[User]:
#     stmt = select(User).order_by(User.id)
#     result = await session.scalars(stmt)
#     return list(result.all())
