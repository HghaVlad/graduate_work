from typing import Annotated
from datetime import datetime, timezone

from fastapi import (
    Depends,
    Path,
    status,
    HTTPException
)
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User
from src.schemas.user import (
    UserCreate,
    UserSocialAccountCreate,
    UserRead,
    UserUpdate
)
from src.db.postgres import db_helper
from src.services import rabbitmq


async def get_users(session: AsyncSession) -> list[User]:
    stmt = select(User).order_by(User.username)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return users


async def get_user(session: AsyncSession, user_id: str) -> User | None:
    return await session.get(User, user_id)


async def get_user_by_id(
    user_id: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.get_session)
) -> User:
    user = await get_user(session, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with ID "{user_id}" was not found'
        )

    return user


async def create_user(
    session: AsyncSession,
    user_in: UserCreate | UserSocialAccountCreate
) -> UserRead:
    # user_in_json = jsonable_encoder(user_in)
    # user = User(**user_in_json)
    user = User(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)

    rabbitmq.send_message_using_routing_key(
        # connection=rabbitmq.rabbitmq_connection,
        exchange_name=rabbitmq.UserActivityExchange.EXCHANGE_NAME.value,
        routing_key=rabbitmq.UserActivityExchange.REGISTRATION_ACTIVITY_ROUTING_KEY.value,
        message={
            'user_id': str(user.id),
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'timestamp': datetime.now(timezone.utc).strftime('%d-%m-%YYYY %H:%M:%S %z')
        }
    )
    return user


async def update_user(
    session: AsyncSession,
    user: User,
    user_update: UserUpdate
) -> UserRead:
    for name, value in user_update.model_dump(exclude_unset=True).items():
        if name == 'password':
            value = user.get_hashed_password(value)
        setattr(user, name, value)
    await session.commit()
    return user


async def delete_user(
    session: AsyncSession,
    user: User,
) -> None:
    await session.delete(user)
    await session.commit()
