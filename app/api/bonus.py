# api/v1/bonus_routes.py
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from app.schemas.bonus import BonusCreate, BonusResponse
from app.services.bonus import distribute_referral_bonus, get_all_bonuses, get_user_bonuses, mark_all_bonuses_as_paid, mark_bonus_as_paid
from app.core.database import get_db

router = APIRouter()

@router.post("/")
def trigger_bonus(payload: BonusCreate, db: Session = Depends(get_db)):
    distribute_referral_bonus(db, payload)
    return {"detail": "Bonuses distributed"}

@router.get("/user/{user_id}", response_model=List[BonusResponse])
def get_user_bonus_history(user_id: UUID = Path(...), db: Session = Depends(get_db)):
    return get_user_bonuses(db, user_id)

@router.get("/", response_model=List[BonusResponse])
def list_all_bonuses(status: Optional[str] = Query(None), db: Session = Depends(get_db)):
    return get_all_bonuses(db, status)

@router.patch("/{bonus_id}/mark-paid", response_model=BonusResponse)
def mark_bonus_paid(bonus_id: UUID, db: Session = Depends(get_db)):
    return mark_bonus_as_paid(db, bonus_id)

@router.get("/mark-paid/all", response_model=List[BonusResponse])
def mark_all_bonuses_paid(db: Session = Depends(get_db)):
    mark_all_bonuses_as_paid(db)
    return {"detail": "All unpaid bonuses marked as paid"}