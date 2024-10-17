from datetime import datetime

from sqlalchemy import DateTime, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from passlib.context import CryptContext

from src.models.base import Base
from src.models.refresh_token import RefreshToken
from src.models.entry_history import EntryHistory


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(32), unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False, server_default='0')
    is_staff: Mapped[bool] = mapped_column(Boolean(), default=False, server_default='0')
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True, server_default='1')
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )

    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(
        back_populates='user',
        passive_deletes=True
    )

    entry_histories: Mapped[list["EntryHistory"]] = relationship(
        back_populates='user',
        passive_deletes=True
    )

    repr_columns = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name'
    )

    def __init__(
            self,
            username: str,
            password: str,
            first_name: str,
            last_name: str,
            email: str,
            is_active: bool = True,
            is_staff: bool = False,
            is_superuser: bool = False
    ) -> None:
        self.username = username
        self.password = self.get_hashed_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_active = is_active
        self.is_staff = is_staff
        self.is_superuser = is_superuser

    def get_hashed_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
