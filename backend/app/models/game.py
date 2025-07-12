from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional, Dict, Any
import enum

class GameStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"

class GameType(str, enum.Enum):
    LOTTERY = "lottery"
    CASINO = "casino"
    SPORTS = "sports"
    POKER = "poker"

class Game(Document):
    name: str
    description: Optional[str] = None
    game_type: GameType
    min_bet: float = 1.0
    max_bet: float = 10000.0
    house_edge: float = 2.0 # percentage
    status: GameStatus = GameStatus.ACTIVE
    is_featured: bool = False
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "games"
        indexes = [
            "name",
            "game_type",
            "status",
        ]

class GameSession(Document):
    game_id: str
    session_data: Optional[Dict[str, Any]] = None # JSON data for game state
    started_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    total_bets: float = 0.0
    total_payouts: float = 0.0

    class Settings:
        name = "game_sessions"
        indexes = [
            "game_id",
            "started_at",
        ]
