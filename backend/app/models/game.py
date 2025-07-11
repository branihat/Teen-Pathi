from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class GameStatus(enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"

class GameType(enum.Enum):
    LOTTERY = "lottery"
    CASINO = "casino"
    SPORTS = "sports"
    POKER = "poker"

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    game_type = Column(Enum(GameType), nullable=False)
    min_bet = Column(Float, default=1.0)
    max_bet = Column(Float, default=10000.0)
    house_edge = Column(Float, default=2.0)  # percentage
    status = Column(Enum(GameStatus), default=GameStatus.ACTIVE)
    is_featured = Column(Boolean, default=False)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    bets = relationship("Bet", back_populates="game")
    game_sessions = relationship("GameSession", back_populates="game")

class GameSession(Base):
    __tablename__ = "game_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"))
    session_data = Column(Text)  # JSON data for game state
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True), nullable=True)
    total_bets = Column(Float, default=0.0)
    total_payouts = Column(Float, default=0.0)
    
    # Relationships
    game = relationship("Game", back_populates="game_sessions")
    bets = relationship("Bet", back_populates="game_session")
