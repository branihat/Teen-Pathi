from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId
import enum

class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    BET_PLACED = "bet_placed"
    BET_WON = "bet_won"
    BET_REFUND = "bet_refund"
    BONUS = "bonus"
    COMMISSION = "commission"

class TransactionStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class PaymentMethod(str, enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    CRYPTO = "crypto"
    WALLET = "wallet"

class Transaction(Document):
    user_id: ObjectId
    transaction_type: TransactionType
    amount: float
    balance_before: float
    balance_after: float
    payment_method: Optional[PaymentMethod] = None
    status: TransactionStatus = TransactionStatus.PENDING
    description: Optional[str] = None
    reference_id: Indexed(Optional[str], unique=True) = None  # External payment reference
    payment_gateway_response: Optional[Dict[str, Any]] = None  # JSON response from payment gateway
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None
    
    class Settings:
        name = "transactions"
        indexes = [
            "user_id",
            "transaction_type",
            "status",
            "created_at",
            "reference_id",
        ]
