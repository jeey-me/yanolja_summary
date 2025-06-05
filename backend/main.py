
# main.py
from fastapi import FastAPI, Depends, HTTPException, Query, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

from database import engine, sessionlocal
from sqlalchemy.orm import Session
import models, schemas


# models에 정의한 모든 클래스, 연결한 DB엔진에 테이블로 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="숙소 리뷰 요약 서비스 API")

# CORS 설정 (Streamlit과 통신을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# html 템플릿 폴더를 지정하여 jinja템플릿 객체 생성
# templates = Jinja2Templates(directory="templates")

# static 폴더(정적파일 폴더)를 app에 연결
app.mount("/static", StaticFiles(directory="static"), name="static")

def get_db():
    db = sessionlocal()
    try:
        # yield 키워드는 FastAPI가 함수의 실행을 일시 중지하고 데이터베이스 세션을 호출자에게 반환하도록 지시
        yield db
    finally:
        # 마지막에 무조건 닫음
        db.close()

@app.get("/")
# async def home(request: Request):
async def home(request: Request, db: Session = Depends(get_db)):
    # accommodation_info에서 ID정보와 이름 정보를 가져오기
    accommodation_list = db.query(models.AccommodationInfo.id, models.AccommodationInfo.name).all()

    # 튜플을 딕셔너리 리스트로 변환
    accommodation_list = [{"id": item[0], "name": item[1]} for item in accommodation_list]
    # for accommodation in accommodation_list:
    #     print(f"숙소 ID: {accommodation['id']}, 숙소 이름: {accommodation['name']}")
    return accommodation_list
 
@app.get("/review_summary/{id}")
async def home(request: Request, id: int , db: Session = Depends(get_db)):
    print("id : ", id)
    # 폼에서 숙소 ID를 가져옴
    review = db.query(models.ReviewSummary).filter(models.ReviewSummary.id == id).order_by(models.ReviewSummary.id.desc()).first()
    # Pydantic 스키마 객체로 변환
    review_response = schemas.ReviewSummaryResponse(
            id=review.id,
            accommodation_id=review.accommodation_id,
            summary_good=review.summary_good,
            summary_bad=review.summary_bad,
            date=review.date,
            )
    return review_response