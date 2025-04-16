# schemas/bonus.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Literal

class BonusCreate(BaseModel):
    source_user_id: UUID
    trigger_type: Literal["referral", "purchase"]

class BonusResponse(BaseModel):
    id: UUID
    user_id: UUID
    source_user_id: UUID
    level: int
    amount: float
    type: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True
