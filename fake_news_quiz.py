import streamlit as st
import openai
import os
import json

# OpenAI API Key 불러오기
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="가짜 뉴스 퀴즈", page_icon="📰", layout="centered")

st.title("📰 가짜 뉴스 퀴즈 & 피드백")
st.markdown("경제 뉴스 중 가짜 뉴스를 판별해보세요. 선택 후 AI가 정답과 피드백을 제공합니다.")

def generate_fake_news():
    prompt = """
    당신은 미디어 리터러시 교육용 가짜 뉴스 생성기입니다.
    - 주제: 경제
    - 뉴스 제목과 배경정보(JSON) 생성
    - 내용: 실제 뉴스처럼 보이지만 모두 가짜
    JSON 형식:
    {
        "title": "뉴스 제목",
        "details": "배경정보 (출처, 통계, 전문가 의견 등)"
    }
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": prompt}],
        temperature=0.7
    )
    try:
        news = json.loads(response['choices'][0]['message']['content'])
        return news['title'], news['details']
    except:
        return "뉴스 생성 실패", response['choices'][0]['message']['content']

if 'title' not in st.session_state:
    st.session_state.title, st.session_state.details = generate_fake_news()
    st.session_state.answer_submitted = False
    st.session_state.feedback = ""

st.subheader("뉴스 제목:")
st.write(st.session_state.title)

st.subheader("배경 정보:")
st.write(st.session_state.details)

user_choice = st.radio("이 뉴스를 믿으시나요?", ("예", "아니오"))

if st.button("결과 확인"):
    prompt_feedback = f"""
    뉴스 제목: {st.session_state.title}
    뉴스 내용: {st.session_state.details}
    사용자 선택: {user_choice}
    이 뉴스가 진짜인지 가짜인지 판별하고,
    선택에 대한 평가, 이유, 미디어 리터러시 교육용 해설 작성
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user", "content": prompt_feedback}],
        temperature=0.7
    )
    st.session_state.feedback = response['choices'][0]['message']['content']
    st.session_state.answer_submitted = True

if st.session_state.answer_submitted:
    st.subheader("✅ AI 피드백 & 해설")
    st.write(st.session_state.feedback)

if st.button("새 문제"):
    st.session_state.title, st.session_state.details = generate_fake_news()
    st.session_state.answer_submitted = False
    st.session_state.feedback = ""
