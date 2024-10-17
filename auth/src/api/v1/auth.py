from datetime import datetime

from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
    Form,
    Request,
    Response
)
from fastapi.security import (
    HTTPBearer,
    OAuth2PasswordBearer
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, Result
from redis.asyncio import Redis

from src.utils import auth_token_utils
from src.schemas.token import Token
from src.db.postgres import db_helper
from src.db.redis import get_redis
from src.models.user import User
from src.models.refresh_token import RefreshToken
from src.models.user_social_account import UserSocialAccount
from src.utils.decorators import rate_limit
from src.utils.auth_utils import (
    get_user_by_username_or_raise_exception,
    parse_request_user_agent_information,

)

http_bearer = HTTPBearer(auto_error=False)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/auth/login/')

router = APIRouter(dependencies=[Depends(http_bearer)])


@router.post('/login/')
@rate_limit()
async def auth_user_issue_jwt(
    request: Request,
    response: Response,
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.get_session),
):
    '''
        Login user by username and password forms:

        Parameters:
            **username** (str): user username
            **password** (str): user password

        Return value:
            **token** (Token): token with the following fields:
            access_token, refresh_token, token_type
    '''
    user: User = await get_user_by_username_or_raise_exception(
        username,
        password,
        session
    )

    await parse_request_user_agent_information(
        request,
        session,
        user
    )

    access_token = await auth_token_utils.create_access_token(
        user,
        session=session
    )
    refresh_token = await auth_token_utils.create_refresh_token(
        user,
        session
    )

    # response.headers['Authorization'] = 'Bearer ' + access_token
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


def get_current_token_payload(
    token: str = Depends(oauth2_scheme)
) -> dict:
    try:
        payload = auth_token_utils.decode_jwt(
            token
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token error'
        )
    return payload


@router.post('/logout/', status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(
    redis: Redis = Depends(get_redis),
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.get_session)

):
    '''
        Logout user
    '''
    user_id = payload['user_id']
    first_name = payload['first_name']
    last_name = payload['last_name']

    token_id = payload['jti']
    token_expires_in = int(
        payload['exp'] - datetime.now().timestamp() + 3
    )

    stmt = delete(RefreshToken).where(RefreshToken.user_id == user_id)
    await session.execute(stmt)
    await session.commit()

    await redis.setex(
        token_id,
        token_expires_in,
        f'User(user_id={user_id}, first_name={first_name}, '
        f'last_name={last_name}, logout_at={datetime.now()})'
    )


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.get_session)
):
    id = payload['user_id']
    token_type = payload.get(auth_token_utils.TOKEN_TYPE_FIELD)

    if token_type != auth_token_utils.ACCESS_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                f'invalid token type {token_type!r} '
                f'expected {auth_token_utils.ACCESS_TOKEN_TYPE!r}'
            )
        )

    stmt = select(User).where(User.id == id)
    result: Result = await session.execute(stmt)
    user: User = result.scalars().first()

    if not user:
        stmt = select(UserSocialAccount).where(UserSocialAccount.id == id)
        result: Result = await session.execute(stmt)
        user: User = result.scalars().first()

    return user


async def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.get_session)
):
    id = payload['user_id']
    token_type = payload.get(auth_token_utils.TOKEN_TYPE_FIELD)

    if token_type != auth_token_utils.REFRESH_TOKEN_TYPE:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=(
                f'invalid token type {token_type!r} '
                f'expected {auth_token_utils.REFRESH_TOKEN_TYPE!r}'
            )
        )
    stmt = select(User).where(User.id == id)
    result: Result = await session.execute(stmt)
    user: User = result.scalar()
    return user


@router.post('/refresh/', response_model=Token)
async def get_auth_refresh_jwt(
    user: User = Depends(get_current_auth_user_for_refresh),
    session: AsyncSession = Depends(db_helper.get_session)
) -> Token:
    '''
        Refresh access and refresh tokens
    '''
    access_token = await auth_token_utils.create_access_token(
        user,
        session
    )
    refresh_token = await auth_token_utils.create_refresh_token(
        user,
        session
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )
