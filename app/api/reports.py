from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.services.weekly_report import get_weekly_bonus_summary
from app.core.database import get_db

router = APIRouter()

@router.get("/weekly/{user_id}")
def weekly_bonus_report(user_id: UUID, db: Session = Depends(get_db)):
    return get_weekly_bonus_summary(db, user_id)
