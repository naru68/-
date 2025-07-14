import streamlit as st

st.set_page_config(page_title="MBTI 직업 추천기", page_icon="🧠")

st.title("🧠 MBTI 기반 직업 추천기")
st.write("당신의 MBTI 유형을 선택하면, 적합한 직업 3가지를 추천해드립니다.")

# MBTI 리스트
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# 직업 추천 사전
mbti_jobs = {
    "INTJ": ["전략기획가", "데이터 과학자", "연구원"],
    "INTP": ["이론 물리학자", "개발자", "컨설턴트"],
    "ENTJ": ["경영 컨설턴트", "CEO", "프로젝트 매니저"],
    "ENTP": ["스타트업 창업자", "마케팅 디렉터", "기획자"],
    "INFJ": ["상담사", "작가", "심리학자"],
    "INFP": ["예술가", "시나리오 작가", "사회복지사"],
    "ENFJ": ["교사", "코치", "홍보 담당자"],
    "ENFP": ["크리에이티브 디렉터", "여행 작가", "기획자"],
    "ISTJ": ["회계사", "공무원", "품질 관리자"],
    "ISFJ": ["간호사", "초등교사", "행정직"],
    "ESTJ": ["군인", "매니저", "감독관"],
    "ESFJ": ["사회복지사", "간호사", "세일즈 매니저"],
    "ISTP": ["엔지니어", "기술자", "파일럿"],
    "ISFP": ["플로리스트", "디자이너", "사진작가"],
    "ESTP": ["영업직", "기업가", "스포츠 코치"],
    "ESFP": ["연예인", "이벤트 플래너", "유튜버"]
}

# 사용자 입력
selected_mbti = st.selectbox("MBTI를 선택하세요", mbti_types)

# 결과 출력
if selected_mbti:
    st.subheader(f"🧩 {selected_mbti} 유형 추천 직업")
    jobs = mbti_jobs.get(selected_mbti, [])
    for i, job in enumerate(jobs, start=1):
        st.write(f"{i}. {job}")
