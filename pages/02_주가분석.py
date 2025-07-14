plotly
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# KOSPI100 일부 종목 (필요하면 전체 넣어줄게)
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

# UI
st.title("📈 KOSPI 100 주가 비교 웹앱 (Plotly 버전)")
st.write("KOSPI 100 종목 중 2개를 선택해서 주가 및 수익률을 비교해보세요.")

stock1_name = st.selectbox("📌 첫 번째 종목", list(kospi100.keys()))
stock2_name = st.selectbox("📌 두 번째 종목", list(kospi100.keys()), index=1)
period = st.selectbox("📅 조회 기간", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

ticker1 = kospi100[stock1_name]
ticker2 = kospi100[stock2_name]

# 데이터 가져오기
data = yf.download([ticker1, ticker2], period=period)["Adj Close"]
data.dropna(inplace=True)
returns = data / data.iloc[0] * 100  # 누적 수익률

# --- Plotly 그래프 ---
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=returns.index,
    y=returns[ticker1],
    mode='lines',
    name=stock1_name,
    line=dict(color='blue')
))

fig.add_trace(go.Scatter(
    x=returns.index,
    y=returns[ticker2],
    mode='lines',
    name=stock2_name,
    line=dict(color='red')
))

fig.update_layout(
    title="📊 누적 수익률 비교 (기준일 대비 %)",
    xaxis_title="날짜",
    yaxis_title="수익률 (%)",
    legend=dict(x=0, y=1),
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# --- 기업 정보 ---
st.subheader("📌 주요 지표 비교")

def get_info(ticker):
    info = yf.Ticker(ticker).info
    return {
        "시가총액": f"{info.get('marketCap', 'N/A'):,}",
        "PER": info.get('trailingPE', 'N/A'),
        "PBR": info.get('priceToBook', 'N/A'),
        "배당수익률": info.get('dividendYield', 'N/A'),
        "산업": info.get('industry', 'N/A')
    }

info1 = get_info(ticker1)
info2 = get_info(ticker2)

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {stock1_name}")
    for k, v in info1.items():
        st.write(f"**{k}:** {v}")

with col2:
    st.markdown(f"### {stock2_name}")
    for k, v in info2.items():
        st.write(f"**{k}:** {v}")

st.caption("📉 데이터 출처: Yahoo Finance (실시간이 아닐 수 있음)")
