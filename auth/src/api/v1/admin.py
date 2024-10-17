from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    Body,
    HTTPException,
    status
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.db.postgres import db_helper
from src.schemas.user import UserReadBySuperUser
from src.models.user_roles import DefaultRoleEnum
from src.models.user import User
from src.utils.decorators import permission_required


http_bearer = HTTPBearer()
router = APIRouter()


@router.post('/users/{user_id}/add-role')
@permission_required(role_required=DefaultRoleEnum.SUPER_USER)
async def add_user_role(
    user_id: Annotated[str, Path],
    role_name: Annotated[str, Body],
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(db_helper.get_session)
):
    '''
        Add a role to an user:

        Parameters:
            **user_id** (str): user id
            **role_name** (str): role name ("super_user", "admin"
            or "public_user")
    '''
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' was not found"
        )

    message = ''

    if role_name == DefaultRoleEnum.SUPER_USER.value:
        if user.is_superuser:
            message = f"{user} already have '{role_name}' permission."
        else:
            user.is_superuser = True
            message = f"'{role_name}' permissions was added to {user}."

    elif role_name == DefaultRoleEnum.ADMIN.value:
        if user.is_staff:
            message = f"{user} already have '{role_name}' permission."
        else:
            user.is_staff = True
            message = f"'{role_name}' permissions was added to {user}."

    elif role_name == DefaultRoleEnum.PUBLIC_USER.value:
        if user.is_active:
            message = f"{user} already have '{role_name}' permission."
        else:
            user.is_active = True
            message = f"'{role_name}' permissions was added to {user}."

    await session.commit()

    user_dto = UserReadBySuperUser.model_validate(user, from_attributes=True)
    user_dict = user_dto.model_dump()

    return {
        'messsage': message,
        'user': user_dict
    }


@router.delete('/users/{user_id}/delete-role')
@permission_required(role_required=DefaultRoleEnum.SUPER_USER)
async def delete_user_role(
    user_id: Annotated[str, Path],
    role_name: Annotated[str, Body],
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(db_helper.get_session)
):
    '''
        Delete role from user:

        Parameters:
            **user_id** (str): user id
            **role_name** (str): role name ("super_user", "admin"
            or "simple_user")
    '''
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' was not found"
        )

    message = ''

    if role_name == DefaultRoleEnum.SUPER_USER.value:
        if not user.is_superuser:
            message = f"{user} have not '{role_name}' permission."
        else:
            user.is_superuser = False
            message = f"'{role_name}' permissions was removed from {user}."

    elif role_name == DefaultRoleEnum.ADMIN.value:
        if user.is_staff:
            message = f"{user} have not '{role_name}' permission."
        else:
            user.is_staff = True
            message = f"'{role_name}' permissions was removed from {user}."

    elif role_name == DefaultRoleEnum.PUBLIC_USER.value:
        if user.is_active:
            message = f"{user} have not '{role_name}' permission."
        else:
            user.is_active = True
            message = f"'{role_name}' permissions was removed from {user}."

    await session.commit()

    user_dto = UserReadBySuperUser.model_validate(user, from_attributes=True)
    user_dict = user_dto.model_dump()

    return {
        'messsage': message,
        'user': user_dict
    }
