from datetime import datetime

from pydantic import BaseModel


class EntryHistoryRead(BaseModel):
    OS: str
    browser: str
    logged_in_at: datetime
