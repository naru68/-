import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# KOSPI 100 일부 종목 (원하는 대로 추가 가능)
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

st.title("📈 KOSPI 100 주가 비교 Plotly 웹앱")

# 종목 선택 UI
stock1_name = st.selectbox("첫 번째 종목 선택", list(kospi100.keys()))
stock2_name = st.selectbox("두 번째 종목 선택", list(kospi100.keys()), index=1)
period = st.selectbox("기간 선택", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

# 티커 매핑
ticker1 = kospi100[stock1_name]
ticker2 = kospi100[stock2_name]
tickers = [ticker1, ticker2]

# 데이터 다운로드
raw_data = yf.download(tickers, period=period)

# 'Adj Close' 또는 'Close' 컬럼 안전하게 추출
if isinstance(raw_data.columns, pd.MultiIndex):
    if "Adj Close" in raw_data.columns.get_level_values(0):
        data = raw_data["Adj Close"]
    elif "Close" in raw_data.columns.get_level_values(0):
        data = raw_data["Close"]
        st.warning("⚠️ 'Adj Close'가 없어 'Close' 데이터를 대신 사용합니다.")
    else:
        st.error("❗ 'Adj Close'나 'Close' 데이터가 없습니다. 다른 종목을 선택하세요.")
        st.stop()
else:
    if "Adj Close" in raw_data.columns:
        data = raw_data[["Adj Close"]]
        data.columns = [tickers[0]]
    elif "Close" in raw_data.columns:
        data = raw_data[["Close"]]
        data.columns = [tickers[0]]
        st.warning("⚠️ 'Adj Close'가 없어 'Close' 데이터를 대신 사용합니다.")
    else:
        st.error("❗ 유효한 주가 데이터가 없습니다.")
        st.stop()

data.dropna(inplace=True)
returns = data / data.iloc[0] * 100

# Plotly 그래프 생성
fig = go.Figure()
for ticker, name, color in zip(data.columns, [stock1_name, stock2_name], ['blue', 'red']):
    fig.add_trace(go.Scatter(
        x=returns.index,
        y=returns[ticker],
        mode='lines',
        name=name,
        line=dict(color=color)
    ))

fig.update_layout(
    title="📊 기준일 대비 누적 수익률 (%) 비교",
    xaxis_title="날짜",
    yaxis_title="수익률 (%)",
    template="plotly_white",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# 주요 지표 표시
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
