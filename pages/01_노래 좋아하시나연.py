import streamlit as st

st.set_page_config(page_title="MBTI 음악 추천기", page_icon="🎵")

st.title("🎵 MBTI & 음악장르 기반 뮤지션 3인 추천기")
st.write("MBTI와 음악 장르를 선택하면 어울리는 뮤지션 3명과 그들의 대표곡을 소개해드려요!")

# 선택 옵션
genres = ["힙합", "발라드", "락", "재즈"]
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# (장르, MBTI): [뮤지션 3명 정보]
recommendations = {
    ("힙합", "INTP"): [
        {
            "name": "타블로 (Epik High)",
            "song": "Fly",
            "desc": "깊이 있는 철학적 가사로 INTP의 분석적인 성향과 어울려요."
        },
        {
            "name": "RM (BTS)",
            "song": "mono.",
            "desc": "내향적이면서도 지적인 면모를 음악으로 풀어내는 아티스트예요."
        },
        {
            "name": "Kendrick Lamar",
            "song": "HUMBLE.",
            "desc": "사회와 인간에 대한 고민을 담은 음악으로 사고가 깊은 INTP와 잘 맞아요."
        }
    ],
    ("발라드", "INFJ"): [
        {
            "name": "폴킴",
            "song": "너를 만나",
            "desc": "따뜻한 감정과 진심을 담은 노래가 INFJ의 섬세함과 잘 어울려요."
        },
        {
            "name": "이수 (M.C the Max)",
            "song": "어디에도",
            "desc": "깊은 감성의 보이스와 진중한 발라드로 INFJ의 감정선을 자극해요."
        },
        {
            "name": "Adele",
            "song": "Someone Like You",
            "desc": "감정의 깊이를 노래하는 아티스트로, INFJ의 내면과 연결돼요."
        }
    ],
    ("락", "ENTP"): [
        {
            "name": "프레디 머큐리 (Queen)",
            "song": "Bohemian Rhapsody",
            "desc": "창의성과 무대 장악력이 뛰어나 ENTP의 에너지와 닮았어요."
        },
        {
            "name": "YB (윤도현밴드)",
            "song": "나는 나비",
            "desc": "자유와 도전의 메시지를 락으로 표현해 ENTP와 잘 맞아요."
        },
        {
            "name": "Green Day",
            "song": "Basket Case",
            "desc": "유쾌하면서도 반항적인 성격이 ENTP의 본성과 연결돼요."
        }
    ],
    ("재즈", "ISFP"): [
        {
            "name": "빌리 홀리데이",
            "song": "Strange Fruit",
            "desc": "감성적이고 예술적인 감각이 뛰어나 ISFP의 섬세함과 어울려요."
        },
        {
            "name": "Norah Jones",
            "song": "Don't Know Why",
            "desc": "잔잔한 분위기와 따뜻한 감성이 조화를 이루는 아티스트예요."
        },
        {
            "name": "Jamie Cullum",
            "song": "Everlasting Love",
            "desc": "감각적인 재즈 연주와 보컬로 ISFP의 감성을 자극해요."
        }
    ]
}

# 사용자 선택
selected_genre = st.selectbox("🎧 음악 장르를 선택하세요", genres)
selected_mbti = st.selectbox("🎭 자신의 MBTI를 선택하세요", mbti_types)

# 결과 출력
key = (selected_genre, selected_mbti)
if key in recommendations:
    st.subheader(f"🎤 '{selected_genre}' 장르 + {selected_mbti} 유형 추천 뮤지션")
    for i, artist in enumerate(recommendations[key], 1):
        st.markdown(f"**{i}. {artist['name']}**")
        st.write(f"대표곡: *{artist['song']}*")
        st.write(f"설명: {artist['desc']}")
        st.markdown("---")
else:
    st.info("이 조합에 대한 추천은 아직 준비 중이에요. 다른 조합을 골라보세요!")
