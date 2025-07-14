# 종목 선택
stock1_name = st.selectbox("첫 번째 종목", list(kospi100.keys()))
stock2_name = st.selectbox("두 번째 종목", list(kospi100.keys()), index=1)

# 여기서 ticker1, ticker2를 지정해야 함
ticker1 = kospi100[stock1_name]
ticker2 = kospi100[stock2_name]

# ✅ 이제 이 시점 이후에 tickers 리스트 생성
tickers = [ticker1, ticker2]

# 그다음에 다운로드 코드 실행
raw_data = yf.download(tickers, period=period)
