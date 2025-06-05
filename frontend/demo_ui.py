import streamlit as st
import requests
import json
from datetime import datetime
import pandas as pd

# FastAPI 백엔드 URL 설정
BASE_URL = "http://localhost:8000"  # FastAPI 서버 주소

# 페이지 설정
st.set_page_config(
    page_title="숙소 리뷰 요약 서비스",
    page_icon="🏨",
    layout="wide"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E86AB;
        margin-bottom: 2rem;
    }
    .accommodation-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2E86AB;
    }
    .summary-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .good-summary {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .bad-summary {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .review-date {
        color: #6c757d;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)

def get_accommodations():
    """백엔드에서 숙소 목록을 가져오는 함수"""
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"숙소 목록을 불러오는데 실패했습니다. 상태 코드: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"서버에 연결할 수 없습니다: {str(e)}")
        return []

def get_review_summary(accommodation_id):
    """특정 숙소의 리뷰 요약을 가져오는 함수"""
    try:
        response = requests.get(f"{BASE_URL}/review_summary/{accommodation_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"리뷰 요약을 불러오는데 실패했습니다. 상태 코드: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"서버에 연결할 수 없습니다: {str(e)}")
        return None

def main():
    # 메인 헤더
    st.markdown('<h1 class="main-header">🏨 숙소 리뷰 요약 서비스</h1>', unsafe_allow_html=True)
    
    # # 사이드바에 설정 옵션
    # st.sidebar.title("설정")
    # st.sidebar.info("백엔드 서버가 실행 중인지 확인하세요.")
    
    # 서버 상태 확인
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            st.sidebar.success("✅ 서버 연결 성공")
        else:
            st.sidebar.error("❌ 서버 연결 실패")
    except:
        st.sidebar.error("❌ 서버에 연결할 수 없습니다")
    
    # 숙소 목록 가져오기
    accommodations = get_accommodations()
    
    if not accommodations:
        st.warning("숙소 목록을 불러올 수 없습니다. 서버 상태를 확인해주세요.")
        return
    
    # 메인 화면에서 숙소 선택 및 리뷰 요약
    st.header("숙소 리뷰 요약")
    
    # 숙소 선택 콤보박스 (selectbox)
    accommodation_options = ["숙소를 선택하세요..."] + [acc['name'] for acc in accommodations]
    selected_name = st.selectbox(
        "🏨 숙소를 선택하세요:",
        options=accommodation_options,
        index=0
    )
    
    # 숙소가 선택되었을 때
    if selected_name != "숙소를 선택하세요...":
        # 선택된 숙소의 ID 찾기
        selected_accommodation = next((acc for acc in accommodations if acc['name'] == selected_name), None)
        
        if selected_accommodation:
            selected_id = selected_accommodation['id']
            
            # 선택된 숙소 정보 표시
            st.info(f"선택된 숙소: **{selected_name}** (ID: {selected_id})")
            
            # 리뷰 요약 버튼
            if st.button("🔍 리뷰 요약 가져오기", type="primary"):
                with st.spinner("리뷰 요약을 불러오는 중..."):
                    review_data = get_review_summary(selected_id)
                    
                    if review_data:
                        # st.success("")
                        
                        # 리뷰 요약 표시
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("""
                            <div class="summary-box good-summary">
                                <h4>😊 긍정적인 리뷰 요약</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            st.write(review_data.get('summary_good', '긍정적인 리뷰가 없습니다.'))
                        
                        with col2:
                            st.markdown("""
                            <div class="summary-box bad-summary">
                                <h4>😞 부정적인 리뷰 요약</h4>
                            </div>
                            """, unsafe_allow_html=True)
                            st.write(review_data.get('summary_bad', '부정적인 리뷰가 없습니다.'))
                        
                        # 추가 정보
                        st.markdown("---")
                        col3, col4 = st.columns(2)
                        
                        with col3:
                            st.metric("숙소 ID", review_data.get('accommodation_id', 'N/A'))
                        
                        with col4:
                            review_date = review_data.get('date')
                            if review_date:
                                st.metric("요약 날짜", review_date)
                            else:
                                st.metric("요약 날짜", "N/A")
                        
                        # JSON 데이터 표시 (디버깅용)
                        with st.expander("원본 데이터 보기 (개발자용)"):
                            st.json(review_data)
                    
                    else:
                        st.error("리뷰 요약을 불러올 수 없습니다.")
    
    # # 하단에 등록된 숙소 목록 표시
    # st.markdown("---")
    # st.subheader("📋 등록된 숙소 목록")
    
    # # 숙소 목록을 간단한 카드 형태로 표시
    # cols = st.columns(3)  # 3열로 배치
    # for i, acc in enumerate(accommodations):
    #     with cols[i % 3]:
    #         st.markdown(f"""
    #         <div class="accommodation-card">
    #             <h5>🏨 {acc['name']}</h5>
    #             <p><strong>ID:</strong> {acc['id']}</p>
    #         </div>
    #         """, unsafe_allow_html=True)
    
    # # 데이터프레임으로도 표시
    # with st.expander("데이터 테이블로 보기"):
    #     df = pd.DataFrame(accommodations)
    #     st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()