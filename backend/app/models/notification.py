from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId
import enum

class NotificationType(str, enum.Enum):
    GAME_UPDATE = "game_update"
    PROMOTION = "promotion"
    BET_RESULT = "bet_result"
    DEPOSIT_CONFIRMATION = "deposit_confirmation"
    WITHDRAWAL_CONFIRMATION = "withdrawal_confirmation"
    ACCOUNT_UPDATE = "account_update"
    GENERAL = "general"

class NotificationStatus(str, enum.Enum):
    UNREAD = "unread"
    READ = "read"
    ARCHIVED = "archived"

class Notification(Document):
    user_id: ObjectId
    title: str
    message: str
    notification_type: NotificationType
    status: NotificationStatus = NotificationStatus.UNREAD
    is_push_sent: bool = False
    is_email_sent: bool = False
    metadata: Optional[Dict[str, Any]] = None  # JSON data for additional info
    created_at: datetime = Field(default_factory=datetime.utcnow)
    read_at: Optional[datetime] = None
    
    class Settings:
        name = "notifications"
        indexes = [
            "user_id",
            "notification_type",
            "status",
            "created_at",
        ]
