from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .config import settings
from typing import Optional

# MongoDB client
client: Optional[AsyncIOMotorClient] = None

# Get MongoDB client
async def get_database_client() -> AsyncIOMotorClient:
    return client

# Initialize database
async def init_database():
    global client
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    # Import all models here for beanie initialization
    from app.models.user import User
    from app.models.bet import Bet
    from app.models.game import Game
    from app.models.transaction import Transaction
    from app.models.notification import Notification
    
    # Initialize beanie with the models
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[
            User,
            Bet,
            Game,
            Transaction,
            Notification
        ],
    )

# Close database connection
async def close_database():
    if client:
        client.close()
