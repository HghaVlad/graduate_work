from typing import Annotated

from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, or_
from redis.asyncio import Redis
from fastapi_pagination import Page, paginate

from src.db.postgres import db_helper
from src.db.redis import get_redis
from src.schemas.user import (
    UserCreate,
    UserRead,
    UserUpdate
)
from src.schemas.entry_history import EntryHistoryRead
from src.models.user import User
from src.models.user_roles import DefaultRoleEnum
from src.models.entry_history import EntryHistory
from src.utils import user_crud
from src.api.v1.auth import (
    get_current_token_payload,
    get_current_auth_user
)
from src.utils.decorators import permission_required


http_bearer = HTTPBearer()
router = APIRouter()


@router.get('/', response_model=list[UserRead])
@permission_required(role_required=DefaultRoleEnum.ADMIN)
async def get_users(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(db_helper.get_session)
):
    '''
        Get user list:

        Return value:
            **users** (list[UserRead]): list of users with the following
            fields: id, login, first_name, last_name and email
    '''
    return await user_crud.get_users(session)


@router.get('/me/', response_model=UserRead)
@permission_required(role_required=DefaultRoleEnum.PUBLIC_USER)
async def get_auth_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    payload: dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_auth_user),
    redis: Redis = Depends(get_redis)
):
    '''
        Get user information:

        Return value:
            **user** (UserRead): user with the following
            fields: id, login, first_name, last_name and email
    '''
    token_id = payload['jti']
    if await redis.get(token_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token error'
        )

    return user


@router.get('/auth_history/', response_model=Page[EntryHistoryRead])
@permission_required(role_required=DefaultRoleEnum.PUBLIC_USER)
async def get_auth_user_auth_history(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    payload: dict = Depends(get_current_token_payload),
    redis: Redis = Depends(get_redis),
    session: AsyncSession = Depends(db_helper.get_session)
):
    '''
        Get authentication history:

        Parameters:
            **page** (int): page number (default=1)
            **size** (ing): page size (default=50) - the amount
            of authentication history rows

        Return value:
            **items** (list[EntryHistoryRead]): list of user authentication
            history with the following fields: OS, browser, logged in at
            **total** (int): the amount of authentication history rows
            **page** (int): page number
            **size** (int): page size
            **pages** (int): the amount of pages
    '''

    token_id = payload['jti']

    if await redis.get(token_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token error'
        )

    user_id = payload['user_id']

    stmt = select(EntryHistory).where(
        or_(EntryHistory.user_social_account_id == user_id, User.id == user_id)
    )
    result: Result = await session.execute(stmt)
    entry_history = result.scalars().all()

    return paginate(entry_history)


@router.post(
    # '/register/', response_model=UserRead, status_code=status.HTTP_201_CREATED
    '/register/', status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_in: UserCreate,
    session: AsyncSession = Depends(db_helper.get_session)
):
    '''
        Create user:

        Return value:
            **user** (UserRead): user with the following
            fields: username, first_name, last_name and email
    '''
    return await user_crud.create_user(session, user_in)


@router.patch('/{user_id}/', response_model=UserRead)
@permission_required(role_required=DefaultRoleEnum.PUBLIC_USER)
async def update_user_partially(
    user_update: UserUpdate,
    user: Annotated[User, Depends(user_crud.get_user_by_id)],
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(db_helper.get_session)
):
    '''
        Update user partially:

        Parameters:
            **user_id** (str): user id

        Return value:
            **user** (UserRead): user with the following
            fields: id, login, first_name, last_name and email
    '''
    return await user_crud.update_user(
        session=session,
        user=user,
        user_update=user_update
    )


@router.delete('/{user_id}/', status_code=status.HTTP_204_NO_CONTENT)
@permission_required(role_required=DefaultRoleEnum.ADMIN)
async def delete_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    user: User = Depends(user_crud.get_user_by_id),
    session: AsyncSession = Depends(db_helper.get_session)
) -> None:
    '''
        Delete user by user id:

        Parameters:
            **user_id** (str): user id
    '''
    await user_crud.delete_user(
        session=session,
        user=user
    )
