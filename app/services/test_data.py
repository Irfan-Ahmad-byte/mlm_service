import uuid
from sqlalchemy.orm import Session
from app.models.mlm import MLMUser
from app.models.bonus import MLMUserBonus
from app.schemas.mlm import MLMUserCreate
from app.services.bonus import distribute_referral_bonus
from app.schemas.bonus import BonusCreate
from app.services.mlm import create_mlm_user


def add_test_data(db: Session):
    """
    Function to add test data to the database.
    This is useful for setting up a test environment.
    """
    # This function is just a placeholder to show where you would add test data
        
    # Clear tables first (optional)
    db.query(MLMUserBonus).delete()
    db.query(MLMUser).delete()
    db.commit()

    # Base user (root of MLM)
    root_user_id = uuid.uuid4()
    root = MLMUser(user_id=root_user_id, parent_id=None, level=1)
    db.add(root)
    db.commit()
    db.refresh(root)

    print(f"Root user created: {root.user_id}")

    # Add 3 direct children
    children = []
    for i in range(250):
        uid = uuid.uuid4()
        child = MLMUserCreate(user_id=uid, parent_id=root.user_id)
        create_mlm_user(db, child)
        children.append(uid)

    # Add bonus triggers (simulate referrals)
    for child_id in children:
        payload = BonusCreate(source_user_id=child_id, trigger_type="referral")
        distribute_referral_bonus(db, payload)

    print("Test users and bonuses added!")
    return {"message": "Test data added successfully!", "root_user_id": str(root_user_id)}
