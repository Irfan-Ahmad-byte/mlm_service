from typing import List
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException

from app.cache.mlm import get_cached_downline, invalidate_user_cache, set_cached_downline
from app.models.mlm import MLMUser
from app.schemas.mlm import MLMUserCreate, MLMUserResponse
from app.configs.configs import settings

def count_children(db: Session, parent_id: UUID) -> int:
    return db.query(MLMUser).filter(MLMUser.parent_id == parent_id).count()

def find_available_parent(db: Session, root_user_id: UUID) -> MLMUser:
    """
    Traverse MLM tree in breadth-first manner to find the next parent with less than MAX_CHILDREN.
    """
    from collections import deque

    queue = deque()
    root = db.query(MLMUser).filter(MLMUser.user_id == root_user_id).first()

    if not root:
        raise HTTPException(status_code=404, detail="Root user not found")

    queue.append(root)

    while queue:
        current = queue.popleft()

        child_count = count_children(db, current.user_id)
        if child_count < settings.MAX_CHILDREN:
            return current  # Found a parent with space

        # Add current node's children to queue
        children = db.query(MLMUser).filter(MLMUser.parent_id == current.user_id).all()
        queue.extend(children)

    raise HTTPException(status_code=400, detail="No suitable parent found")

def create_mlm_user(db: Session, payload: MLMUserCreate) -> MLMUser:
    existing = db.query(MLMUser).filter(MLMUser.user_id == payload.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists in MLM tree")

    # Step 1: Determine real parent using spillover logic
    parent = None
    level = 1

    if payload.parent_id:
        parent = find_available_parent(db, payload.parent_id)
        level = parent.level + 1

    mlm_user = MLMUser(
        user_id=payload.user_id,
        parent_id=parent.user_id if parent else None,
        level=level
    )
    db.add(mlm_user)
    db.commit()
    db.refresh(mlm_user)

    if parent:
        invalidate_user_cache(parent.user_id)
    
    return mlm_user

def build_user_tree(db: Session, parent_id: UUID) -> List[MLMUserResponse]:
    children = db.query(MLMUser).filter(MLMUser.parent_id == parent_id).all()
    result = []

    for child in children:
        child_schema = MLMUserResponse.from_orm(child)
        child_schema.children = build_user_tree(db, child.user_id)
        result.append(child_schema)

    return result

def get_user_downline(db: Session, user_id: UUID):
    cached = get_cached_downline(str(user_id))
    if cached:
        return cached

    downline_tree = build_user_tree(db, user_id)

    # Optional: serialize before caching
    serialized_tree = [u.model_dump() for u in downline_tree]
    set_cached_downline(str(user_id), serialized_tree)

    return serialized_tree

def cont_user_downline(db: Session, user_id: UUID):
    """
    Count the number of users in the downline of a given user, recursively.
    """
    downline = get_user_downline(db, user_id)
    count = 0

    def count_recursive(users):
        nonlocal count
        for user in users:
            count += 1
            count_recursive(user.children)

    count_recursive(downline)
    return count

def add_root_user_into_db(db: Session, payload: MLMUserCreate) -> MLMUser:
    existing = db.query(MLMUser).filter(MLMUser.user_id == payload.user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Root user already exists in MLM tree")

    mlm_user = MLMUser(
        user_id=payload.user_id,
        parent_id=None,
        level=1
    )
    db.add(mlm_user)
    db.commit()
    db.refresh(mlm_user)

    return mlm_user