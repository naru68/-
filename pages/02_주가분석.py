import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# KOSPI100 티커 목록 (일부 예시만 수록, 실제 앱에선 전체 입력 가능)
kospi100 = {
    "삼성전자": "005930.KS",
    "SK하이닉스": "000660.KS",
    "LG화학": "051910.KS",
    "NAVER": "035420.KS",
    "카카오": "035720.KS",
    "삼성바이오로직스": "207940.KS",
    "현대차": "005380.KS",
    "POSCO홀딩스": "005490.KS"
}

st.title("📈 KOSPI 100 주가 비교 분석")
st.write("KOSPI 100에 속한 주식 2개를 선택해 비교해보세요.")

# 주식 선택
stock1_name = st.selectbox("첫 번째 종목 선택", list(kospi100.keys()))
stock2_name = st.selectbox("두 번째 종목 선택", list(kospi100.keys()), index=1)

# 티커 매핑
ticker1 = kospi100[stock1_name]
ticker2 = kospi100[stock2_name]

# 기간 설정
period = st.selectbox("비교할 기간", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

# 데이터 가져오기
data = yf.download([ticker1, ticker2], period=period)["Adj Close"]
data.dropna(inplace=True)

# 수익률 계산
returns = data / data.iloc[0] * 100

# --- 주가 비교 그래프 ---
st.subheader("📊 주가 비교 (정규화)")
fig, ax = plt.subplots()
returns.plot(ax=ax)
ax.set_ylabel("주가 (기준일 대비 %)")
ax.legend([stock1_name, stock2_name])
st.pyplot(fig)

# --- 주요 지표 출력 ---
st.subheader("📌 주요 정보")
col1, col2 = st.columns(2)

ticker1_info = yf.Ticker(ticker1).info
ticker2_info = yf.Ticker(ticker2).info

with col1:
    st.markdown(f"### {stock1_name}")
    st.write(f"**시가총액:** {ticker1_info.get('marketCap', 'N/A'):,} 원")
    st.write(f"**PER:** {ticker1_info.get('trailingPE', 'N/A')}")
    st.write(f"**PBR:** {ticker1_info.get('priceToBook', 'N/A')}")
    st.write(f"**배당수익률:** {ticker1_info.get('dividendYield', 'N/A')}")

with col2:
    st.markdown(f"### {stock2_name}")
    st.write(f"**시가총액:** {ticker2_info.get('marketCap', 'N/A'):,} 원")
    st.write(f"**PER:** {ticker2_info.get('trailingPE', 'N/A')}")
    st.write(f"**PBR:** {ticker2_info.get('priceToBook', 'N/A')}")
    st.write(f"**배당수익률:** {ticker2_info.get('dividendYield', 'N/A')}")

st.caption("데이터 출처: Yahoo Finance (실시간 데이터 아님)")
