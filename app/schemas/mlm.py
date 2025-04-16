from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class MLMUserCreate(BaseModel):
    user_id: UUID
    parent_id: Optional[UUID] = None

class MLMUserResponse(BaseModel):
    id: UUID
    user_id: UUID
    parent_id: Optional[UUID]
    level: int
    created_at: datetime
    updated_at: Optional[datetime]
    children: List["MLMUserResponse"] = []

    class Config:
        from_attributes = True
