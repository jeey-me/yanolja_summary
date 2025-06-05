
import datetime
import json
import os
import pickle
from dateutil import parser
from openai import OpenAI


# 환경 변수에서 API 키 가져오기
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# 함수가 실행된 결과를 메모리 또는 디스크에 저장
def load_prompt():
    try:
        with open('./res/prompt_1shotv1.pickle', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("프롬프트 파일(prompt_1shotv1.pickle)을 찾을 수 없습니다.")
        return ""
    
# 프롬프트 로드
PROMPT = load_prompt()

def preprocess_reviews(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            review_list = json.load(f)
    except FileNotFoundError:
        print("리뷰 파일을 찾을 수 없습니다:", path)
        return "", ""

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
        if len(r['review']) < 30:
            filtered_cnt += 1
            continue

        # 별점 기준 개선: 4-5점은 좋은 리뷰, 1-3점은 나쁜 리뷰
        if r['stars'] >= 4:
            reviews_good.append('[REVIEW_START]' + r['review'] + '[REVIEW_END]')
        elif r['stars'] <= 3:
            reviews_bad.append('[REVIEW_START]' + r['review'] + '[REVIEW_END]')
        # r['stars']가 없거나 범위를 벗어나면 제외

    reviews_good = reviews_good[:min(len(reviews_good), 50)]
    reviews_bad = reviews_bad[:min(len(reviews_bad), 50)]

    reviews_good_text = '\n'.join(reviews_good)
    reviews_bad_text = '\n'.join(reviews_bad)

    return reviews_good_text, reviews_bad_text


def summarize(reviews):
    """OpenAI API를 사용해 리뷰 요약"""
    prompt = PROMPT + '\n\n' + reviews

    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.0
    )
    return completion