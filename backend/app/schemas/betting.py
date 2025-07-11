from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.game import GameType, GameStatus
from app.models.bet import BetType, BetStatus

# Game Schemas
class GameBase(BaseModel):
    name: str
    description: Optional[str] = None
    game_type: GameType
    min_bet: float = 1.0
    max_bet: float = 10000.0
    house_edge: float = 2.0

class GameCreate(GameBase):
    pass

class GameUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    min_bet: Optional[float] = None
    max_bet: Optional[float] = None
    house_edge: Optional[float] = None
    status: Optional[GameStatus] = None
    is_featured: Optional[bool] = None
    image_url: Optional[str] = None

class GameResponse(GameBase):
    id: int
    status: GameStatus
    is_featured: bool
    image_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# Bet Schemas
class BetBase(BaseModel):
    game_id: int
    bet_amount: float
    odds: float
    bet_type: BetType = BetType.SINGLE
    bet_data: Optional[Dict[str, Any]] = None
    
    @validator('bet_amount')
    def validate_bet_amount(cls, v):
        if v <= 0:
            raise ValueError('Bet amount must be positive')
        return v

class BetCreate(BetBase):
    pass

class BetResponse(BetBase):
    id: int
    user_id: int
    potential_payout: float
    actual_payout: float
    status: BetStatus
    result_data: Optional[Dict[str, Any]] = None
    placed_at: datetime
    settled_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Game Session Schemas
class GameSessionResponse(BaseModel):
    id: int
    game_id: int
    session_data: Optional[Dict[str, Any]] = None
    started_at: datetime
    ended_at: Optional[datetime] = None
    total_bets: float
    total_payouts: float
    
    class Config:
        from_attributes = True

class GameList(BaseModel):
    games: List[GameResponse]
    total: int
    page: int
    size: int

class BetList(BaseModel):
    bets: List[BetResponse]
    total: int
    page: int
    size: int
