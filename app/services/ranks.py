from uuid import UUID
from app.models.ranks import MLMUserRank
from app.models.mlm import MLMUser
from sqlalchemy.orm import Session

# Rank based on downline count (can be extended to bonus amount too)
RANKS = [
    ("Bronze", 3),
    ("Silver", 10),
    ("Gold", 25),
    ("Diamond", 50)
]


def get_downline_count(db: Session, user_id: UUID) -> int:
    return db.query(MLMUser).filter(MLMUser.parent_id == user_id).count()

def evaluate_and_assign_rank(db: Session, user_id: UUID):
    downline_count = get_downline_count(db, user_id)

    # Assign highest applicable rank
    new_rank = None
    for rank, min_count in reversed(RANKS):
        if downline_count >= min_count:
            new_rank = rank
            break

    if not new_rank:
        return None

    existing = db.query(MLMUserRank).filter(MLMUserRank.user_id == user_id).first()
    if existing:
        if existing.rank != new_rank:
            existing.rank = new_rank
            db.commit()
        return existing
    else:
        rank_record = MLMUserRank(user_id=user_id, rank=new_rank)
        db.add(rank_record)
        db.commit()
        return rank_record
