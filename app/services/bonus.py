# services/bonus_logic.py
from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.mlm import MLMUser
from app.models.bonus import MLMUserBonus
from app.schemas.bonus import BonusCreate
from app.utils.logs import get_logger


logger = get_logger(__name__)

BONUS_MAP = {
    1: 10.0,  # Level 1 = $10
    2: 5.0,
    3: 2.0,
    4: 1.0
}
MAX_LEVELS = 4


def distribute_referral_bonus(db: Session, payload: BonusCreate):
    source = db.query(MLMUser).filter(MLMUser.user_id == payload.source_user_id).first()
    if not source:
        logger.error(f"Source user {payload.source_user_id} not found")
        raise ValueError("Source user not found")

    upline_chain = []
    current = source
    level = 0

    # Traverse upline till MAX_LEVELS
    while current.parent_id and level < MAX_LEVELS:
        level += 1
        parent = db.query(MLMUser).filter(MLMUser.user_id == current.parent_id).first()
        if not parent:
            break
        upline_chain.append((parent.user_id, level))
        current = parent

    # Create bonuses
    for uid, lvl in upline_chain:
        bonus_amount = BONUS_MAP.get(lvl, 0.0)
        if bonus_amount > 0:
            bonus = MLMUserBonus(
                user_id=uid,
                source_user_id=payload.source_user_id,
                level=lvl,
                amount=bonus_amount,
                type=payload.trigger_type
            )
            db.add(bonus)

    db.commit()


def get_user_bonuses(db: Session, user_id: UUID):
    return db.query(MLMUserBonus).filter(MLMUserBonus.user_id == user_id).order_by(MLMUserBonus.created_at.desc()).all()


def get_all_bonuses(db: Session, status: Optional[str] = None):
    q = db.query(MLMUserBonus)
    if status:
        q = q.filter(MLMUserBonus.status == status)
    return q.order_by(MLMUserBonus.created_at.desc()).all()


def mark_bonus_as_paid(db: Session, bonus_id: UUID):
    bonus = db.query(MLMUserBonus).filter(MLMUserBonus.id == bonus_id).first()
    if not bonus:
        logger.error(f"Bonus {bonus_id} not found")
        raise HTTPException(status_code=404, detail="Bonus not found")
    bonus.status = "paid"
    db.commit()
    db.refresh(bonus)
    return bonus


def mark_all_bonuses_as_paid(db: Session):
    bonuses = db.query(MLMUserBonus).filter(MLMUserBonus.status == "pending").all()
    for bonus in bonuses:
        bonus.status = "paid"
    db.commit()
    return {"detail": "All unpaid bonuses marked as paid"}