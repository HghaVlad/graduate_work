from functools import wraps
from datetime import datetime

from fastapi import HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
import redis

from src.models.user_roles import DefaultRoleEnum
from src.utils import auth_token_utils
from src.core.config import settings


redis_conn = redis.Redis(
    host=settings.service_settings.redis_host,
    port=settings.service_settings.redis_port,
    db=1
)


def permission_required(role_required: DefaultRoleEnum):
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):

            forbidden_exception = HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail='You don\'t have the appropriate access permissions'
                    )

            credentials: HTTPAuthorizationCredentials = kwargs.get('credentials')
            token = credentials.credentials
            token_payload: dict = auth_token_utils.decode_jwt(token)
            role: str = token_payload.get('role')
            role_list = role.split(' ')

            if role_required == DefaultRoleEnum.SUPER_USER:
                if DefaultRoleEnum.SUPER_USER.value not in role_list:
                    raise forbidden_exception
            elif role_required == DefaultRoleEnum.ADMIN:
                if DefaultRoleEnum.ADMIN.value not in role_list and DefaultRoleEnum.SUPER_USER.value not in role_list:
                    raise forbidden_exception

            return await func(*args, **kwargs)
        return inner
    return func_wrapper


def rate_limit():
    def wrapper(func):
        @wraps(func)
        async def inner(request: Request, *args, **kwargs):
            pipline = redis_conn.pipeline()
            now = datetime.now()
            key = f"{request.headers.get('Origin')}:{now.minute}"
            pipline.incr(key, 1)
            pipline.expire(key, 59)
            request_number = pipline.execute()[0]
            if request_number > settings.REQUEST_LIMIT_PER_MINUTE:
                return HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail='Too Many Requests'
                )
            return await func(request, *args, **kwargs)
        return inner
    return wrapper
