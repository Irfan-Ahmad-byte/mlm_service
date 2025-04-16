from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID
from app.services.ranks import evaluate_and_assign_rank
from app.core.database import get_db

router = APIRouter()

@router.post("/evaluate/{user_id}")
def evaluate_rank(user_id: UUID, db: Session = Depends(get_db)):
    result = evaluate_and_assign_rank(db, user_id)
    return {"message": f"Assigned rank: {result.rank if result else 'No rank'}"}
