from datetime import datetime

from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    id: Optional[int] = None
    title: str
    date: Optional[str] = None
    description: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None