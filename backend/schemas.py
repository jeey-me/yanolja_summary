
# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AccommodationBase(BaseModel):
    name: str
    address: Optional[str] = None
    phone_number: Optional[str] = None
    rating: Optional[float] = None


class ReviewSummaryResponse(BaseModel):
    id: int
    accommodation_id: int
    summary_good: Optional[str] = None
    summary_bad: Optional[str] = None
    date: datetime
    
    class Config:
        from_attributes = True
