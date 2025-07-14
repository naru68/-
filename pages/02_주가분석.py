import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

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
stock1_name = st.selectbox("첫 번째 종목", list(kospi100.keys()))
stock2_name = st.selectbox("두 번째 종목", list(kospi100.keys()), index=1)
period = st.selectbox("기간 선택", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

ticker1 = kospi100[stock1_name]
ticker2 = kospi100[stock2_name]
tickers = [ticker1, ticker2]

# 다운로드
raw_data = yf.download(tickers, period=period)

# 안전하게 'Adj Close' 추출
if isinstance(raw_data.columns, pd.MultiIndex):
    if "Adj Close" in raw_data.columns.get_level_values(0):
        data = raw_data["Adj Close"]
    else:
        st.error("❗ 'Adj Close' 데이터가 존재하지 않습니다.")
        st.stop()
else:
    if "Adj Close" in raw_data.columns:
        data = raw_data[["Adj Close"]]
        data.columns = [tickers[0]]
    else:
        st.error("❗ 'Adj Close' 컬럼을 찾을 수 없습니다.")
        st.stop()

# 정리
data.dropna(inplace=True)
returns = data / data.iloc[0] * 100

# 시각화
fig = go.Figure()
for ticker, name, color in zip(data.columns, [stock1_name, stock2_name], ['blue', 'red']):
    fig.add_trace(go.Scatter(x=returns.index, y=returns[ticker], mode='lines', name=name, line=dict(color=color)))

fig.update_layout(title="📊 기준일 대비 수익률 (%)", xaxis_title="날짜", yaxis_title="수익률", template="plotly_white")
st.plotly_chart(fig, use_container_width=True)
