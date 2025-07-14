import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# KOSPI100 일부
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

st.title("📈 KOSPI 100 주가 비교 웹앱 (Plotly 안정화 버전)")
stock1_name = st.selectbox("📌 첫 번째 종목", list(kospi100.keys()))
stock2_name = st.selectbox("📌 두 번째 종목", list(kospi100.keys()), index=1)
period = st.selectbox("📅 조회 기간", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

ticker1 = kospi100[stock1_name]
ticker2 = kospi100[stock2_name]

# 데이터 다운로드
tickers = [ticker1, ticker2]
raw_data = yf.download(tickers, period=period)

# 데이터 구조에 따라 'Adj Close' 안전하게 추출
if isinstance(raw_data.columns, pd.MultiIndex):
    # 멀티인덱스: (속성, 티커) 구조이므로 이렇게 추출
    data = raw_data['Adj Close']
else:
    # 단일 컬럼: 데이터가 하나만 들어온 경우
    data = raw_data[['Adj Close']]
    data.columns = [tickers[0]]  # 단일 종목일 때는 이름 바꿔줌

# 결측치 제거
data.dropna(inplace=True)

# 수익률 계산 (기준일 대비 %)
returns = data / data.iloc[0] * 100

# Plotly 그래프
fig = go.Figure()
for ticker, name, color in zip([ticker1, ticker2], [stock1_name, stock2_name], ['blue', 'red']):
    if ticker in returns.columns:
        fig.add_trace(go.Scatter(
            x=returns.index,
            y=returns[ticker],
            mode='lines',
            name=name,
            line=dict(color=color)
        ))

fig.update_layout(
    title="📊 누적 수익률 비교 (기준일 대비 %)",
    xaxis_title="날짜",
    yaxis_title="수익률 (%)",
    template="plotly_white",
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

# 기업 정보 비교
st.subheader("📌 주요 지표 비교")

def get_info(ticker):
    try:
        info = yf.Ticker(ticker).info
        return {
            "시가총액": f"{info.get('marketCap', 'N/A'):,}",
            "PER": info.get('trailingPE', 'N/A'),
            "PBR": info.get('priceToBook', 'N/A'),
            "배당수익률": info.get('dividendYield', 'N/A'),
            "산업": info.get('industry', 'N/A')
        }
    except Exception:
        return {
            "시가총액": "N/A",
            "PER": "N/A",
            "PBR": "N/A",
            "배당수익률": "N/A",
            "산업": "N/A"
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

st.caption("📉 데이터 출처: Yahoo Finance")
