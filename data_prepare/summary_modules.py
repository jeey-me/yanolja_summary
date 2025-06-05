import datetime
import pickle
from dateutil import parser
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# prompt 로드 
def load_prompt(data_path):
    try:
        with open(data_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        print("리뷰 파일을 찾을 수 없습니다:")

# 파일 데이터 로딩 및 전처리 
def preprocess_reviews(data_path):
    with open(data_path, 'r', encoding='utf-8') as f:
        review_list = json.load(f)

    reviews_good, reviews_bad = [], []

    current_date = datetime.datetime.now()
    date_boundary = current_date - datetime.timedelta(days=6*30)

    filtered_cnt = 0
    for r in review_list:
        review_date_str = r['date']
        try:
            review_date = parser.parse(review_date_str)
        except (ValueError, TypeError):
            review_date = current_date

        if review_date < date_boundary:
            continue

        # 고품질 리뷰만 남김
        if len(r['review']) < 30:
            filtered_cnt += 1
            # print(r['review'])
            continue

        if r['stars'] == 5:
            reviews_good.append('[REVIEW_START]' + r['review'] + '[REVIEW_END]')
        else:
            reviews_bad.append('[REVIEW_START]' + r['review'] + '[REVIEW_END]')

        # 최대 길이가 50까지 되도로 자름 
        reviews_good = reviews_good[:min(len(reviews_good), 50)]
        reviews_bad = reviews_bad[:min(len(reviews_bad), 50)]

        reviews_good_text = '\n'.join(reviews_good)
        reviews_bad_text = '\n'.join(reviews_bad)

        return reviews_good_text, reviews_bad_text



# LLM을 통한 요약 
def summarize(reviews, prompt, temperature=0.0, model='gpt-3.5-turbo-0125'):

    # 절대경로나 정확한 상대경로 지정
    load_dotenv('C:/Users/Admin/kpmg_future_lab/LLM_ex/yanolja_summary/.env', override=True)

    # 환경 변수에서 API 키 가져오기
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    # print(f"API Key loaded: {OPENAI_API_KEY[:10]}...")  # 앞 10글자만 출력 (확인용)

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=OPENAI_API_KEY)
    prompt = prompt + '\n\n' + reviews

    completion = client.chat.completions.create(
        model=model,
        messages=[{'role': 'user', 'content': prompt}],
        temperature=temperature
    )

    return completion.choices[0].message.content
    

# DB에 저장하기 



