from sqlalchemy import Column, UUID, ForeignKey, String, DateTime, func
from app.core.database import Base
import uuid

class MLMUserRank(Base):
    __tablename__ = "mlm_user_ranks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("mlm_users.user_id"), nullable=False, unique=True)
    rank = Column(String, nullable=False)
    achieved_at = Column(DateTime(timezone=True), server_default=func.now())
