from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, Boolean, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import enum

class BetStatus(enum.Enum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class BetType(enum.Enum):
    SINGLE = "single"
    MULTIPLE = "multiple"
    SYSTEM = "system"

class Bet(Base):
    __tablename__ = "bets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    game_id = Column(Integer, ForeignKey("games.id"))
    game_session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=True)
    bet_amount = Column(Float, nullable=False)
    potential_payout = Column(Float, nullable=False)
    actual_payout = Column(Float, default=0.0)
    odds = Column(Float, nullable=False)
    bet_type = Column(Enum(BetType), default=BetType.SINGLE)
    status = Column(Enum(BetStatus), default=BetStatus.PENDING)
    bet_data = Column(Text)  # JSON data for bet details
    result_data = Column(Text)  # JSON data for bet result
    placed_at = Column(DateTime(timezone=True), server_default=func.now())
    settled_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="bets")
    game = relationship("Game", back_populates="bets")
    game_session = relationship("GameSession", back_populates="bets")
