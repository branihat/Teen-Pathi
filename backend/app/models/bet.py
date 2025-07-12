from beanie import Document, Link
from pydantic import Field
from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId
import enum

class BetStatus(str, enum.Enum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class BetType(str, enum.Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"
    SYSTEM = "system"

class Bet(Document):
    user_id: ObjectId
    game_id: ObjectId
    game_session_id: Optional[ObjectId] = None
    bet_amount: float
    potential_payout: float
    actual_payout: float = 0.0
    odds: float
    bet_type: BetType = BetType.SINGLE
    status: BetStatus = BetStatus.PENDING
    bet_data: Optional[Dict[str, Any]] = None  # JSON data for bet details
    result_data: Optional[Dict[str, Any]] = None  # JSON data for bet result
    placed_at: datetime = Field(default_factory=datetime.utcnow)
    settled_at: Optional[datetime] = None
    
    class Settings:
        name = "bets"
        indexes = [
            "user_id",
            "game_id",
            "status",
            "placed_at",
        ]
