from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.core.deps import get_current_active_user, get_current_admin_user
from app.models.game import Game, GameStatus
from app.schemas.betting import GameCreate, GameUpdate, GameResponse, GameList

router = APIRouter(prefix="/games", tags=["Games"])

@router.get("/", response_model=GameList)
def get_games(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    game_type: Optional[str] = None,
    featured_only: bool = False,
    db: Session = Depends(get_db)
):
    """Get all active games."""
    query = db.query(Game).filter(Game.status == GameStatus.ACTIVE)
    
    if game_type:
        query = query.filter(Game.game_type == game_type)
    
    if featured_only:
        query = query.filter(Game.is_featured == True)
    
    total = query.count()
    games = query.offset(skip).limit(limit).all()
    
    return GameList(
        games=games,
        total=total,
        page=skip // limit + 1,
        size=limit
    )

@router.get("/{game_id}", response_model=GameResponse)
def get_game(game_id: int, db: Session = Depends(get_db)):
    """Get game by ID."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    return game

@router.post("/", response_model=GameResponse, status_code=status.HTTP_201_CREATED)
def create_game(
    game: GameCreate,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Create a new game (admin only)."""
    db_game = Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

@router.put("/{game_id}", response_model=GameResponse)
def update_game(
    game_id: int,
    game_update: GameUpdate,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Update game (admin only)."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    for field, value in game_update.dict(exclude_unset=True).items():
        setattr(game, field, value)
    
    db.commit()
    db.refresh(game)
    return game

@router.delete("/{game_id}")
def delete_game(
    game_id: int,
    current_user = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """Delete game (admin only)."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    db.delete(game)
    db.commit()
    return {"message": "Game deleted successfully"}
