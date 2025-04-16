# models/bonus.py
from sqlalchemy import Column, UUID, String, Float, Integer, DateTime, ForeignKey, func
from app.core.database import Base
import uuid

class MLMUserBonus(Base):
    __tablename__ = "mlm_bonuses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("mlm_users.user_id"), nullable=False)  # bonus receiver
    source_user_id = Column(UUID(as_uuid=True), nullable=False)  # the user who triggered bonus
    level = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    type = Column(String, default="referral")  # can be 'referral', 'rank', 'purchase' etc.
    status = Column(String, default="pending")  # pending, paid
    created_at = Column(DateTime(timezone=True), server_default=func.now())
