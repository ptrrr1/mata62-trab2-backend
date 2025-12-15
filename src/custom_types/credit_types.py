from pydantic import BaseModel
from datetime import datetime


class CreditBuyRequest(BaseModel):
    amount: int


class CreditHistoryResponse(BaseModel):
    amount: int
    created_at: datetime


class CreditHistoryCompleteResponse(BaseModel):
    id: int
    user_id: int
    amount: int
    created_at: datetime
