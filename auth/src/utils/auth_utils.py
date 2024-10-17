from datetime import datetime

from fastapi import HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from uaparser import UAParser

from src.models.user import User
from src.models.user_social_account import UserSocialAccount
from src.models.entry_history import EntryHistory


unauth_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid username or password',
    headers={'WWW-Authenticate': 'Basic'}
)


async def parse_request_user_agent_information(
    request: Request,
    session: AsyncSession,
    user: User | UserSocialAccount
):
    ua_header_data = request.headers.get('User-Agent')
    login_device_information = UAParser.parse(ua_header_data)

    if not login_device_information['device']['type']:
        login_device_information['device']['type'] = 'undefined'

    entry_history_to_db = EntryHistory(
        OS=(
            f"{login_device_information['os']['name']} "
            f"{login_device_information['os']['version']}"
        ),
        browser=(
            f"{login_device_information['browser']['name']} "
        ),
        device_type=login_device_information['device']['type'],
        logged_in_at=datetime.now(),
        user_id=user.id
    )

    session.add(entry_history_to_db)
    await session.commit()
    await session.refresh(entry_history_to_db)


async def get_user_by_username_or_raise_exception(
    username: str,
    password: str,
    session: AsyncSession
):
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user: User | None = result.scalar()

    if not user:
        raise unauth_exception

    if not user.verify_password(
        plain_password=password,
        hashed_password=user.password
    ):
        raise unauth_exception

    return user
