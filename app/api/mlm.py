from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.mlm import MLMUserCreate, MLMUserResponse
from app.services.mlm import add_root_user_into_db, cont_user_downline, create_mlm_user, get_user_downline
from app.core.database import get_db
from uuid import UUID
from typing import List

router = APIRouter()

@router.post("/register", response_model=MLMUserResponse)
def register_user(payload: MLMUserCreate, db: Session = Depends(get_db)):
    return create_mlm_user(db, payload)

@router.get("/downline/{user_id}", response_model=List[MLMUserResponse])
def fetch_downline(user_id: UUID, db: Session = Depends(get_db)):
    return get_user_downline(db, user_id)


@router.get("/downline/{user_id}/count", response_model=int)
def fetch_downline_count(user_id: UUID, db: Session = Depends(get_db)):
    return cont_user_downline(db, user_id)

@router.post("/root_user", response_model=MLMUserResponse)
def add_root_user(payload: MLMUserCreate, db: Session = Depends(get_db)):
    """
    Create a root user in the MLM tree.
    """
    return add_root_user_into_db(db, payload)

@router.get("/add_test_data")
def add_test_data(db: Session = Depends(get_db)):
    """
    Function to add test data to the database.
    This is useful for setting up a test environment.
    """
    from app.services.test_data import add_test_data
    
    return add_test_data(db)