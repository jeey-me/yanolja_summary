
# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# class AccommodationBase(BaseModel):
#     name: str
#     address: Optional[str] = None
#     phone_number: Optional[str] = None
#     rating: Optional[float] = None

# 데이터 전송 객체 = dto(data transfer object) 정의 
# => 리뷰요약 정보를 오브젝트로 리턴 (=클라이언트에 json 객체로 넘어감)
class ReviewSummaryResponse(BaseModel):
    id: int
    accommodation_id: int
    summary_good: Optional[str] = None
    summary_bad: Optional[str] = None
    date: datetime
    
    class Config:
        from_attributes = True
