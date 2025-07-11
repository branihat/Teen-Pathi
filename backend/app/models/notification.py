from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class NotificationType(enum.Enum):
    GAME_UPDATE = "game_update"
    PROMOTION = "promotion"
    BET_RESULT = "bet_result"
    DEPOSIT_CONFIRMATION = "deposit_confirmation"
    WITHDRAWAL_CONFIRMATION = "withdrawal_confirmation"
    ACCOUNT_UPDATE = "account_update"
    GENERAL = "general"

class NotificationStatus(enum.Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType), nullable=False)
    status = Column(Enum(NotificationStatus), default=NotificationStatus.UNREAD)
    is_push_sent = Column(Boolean, default=False)
    is_email_sent = Column(Boolean, default=False)
    metadata = Column(Text, nullable=True)  # JSON data for additional info
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="notifications")
