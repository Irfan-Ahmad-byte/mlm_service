from uuid import UUID
from app.models.bonus import MLMUserBonus
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

def get_weekly_bonus_summary(db: Session, user_id: UUID):
    now = datetime.now(timezone.utc)
    week_ago = now - timedelta(days=7)

    bonuses = db.query(MLMUserBonus).filter(
        MLMUserBonus.user_id == user_id,
        MLMUserBonus.created_at >= week_ago
    ).all()

    total = sum(b.amount for b in bonuses)
    return {
        "user_id": str(user_id),
        "total_bonus": total,
        "count": len(bonuses),
        "bonuses": [b.__dict__ for b in bonuses]
    }
