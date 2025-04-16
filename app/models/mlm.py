from sqlalchemy import Column, Integer, ForeignKey, DateTime, Table, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import declarative_base


from app.db.base_class import Base


Non_Base = declarative_base()
class MLMUser(Non_Base):
    __tablename__ = "mlm_users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), unique=True, nullable=False, index=True)  # From Auth Service
    parent_id = Column(UUID(as_uuid=True), ForeignKey("mlm_users.user_id"))
    level = Column(Integer, default=1)  # MLM Level (depth in tree)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


metadata = Base.metadata
t = Table(
    "mlm_users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
    Column("user_id", UUID(as_uuid=True), nullable=False, unique=True, index=True),
    Column("parent_id", UUID(as_uuid=True), ForeignKey("mlm_users.user_id"), nullable=True),
    Column("level", Integer, default=1),
    Column("created_at", DateTime(timezone=True), server_default=func.now()),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now()),
    UniqueConstraint("user_id"),
)