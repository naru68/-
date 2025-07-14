# 데이터 다운로드
tickers = [ticker1, ticker2]
raw_data = yf.download(tickers, period=period)

# 멀티인덱스 여부 체크
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
    # 싱글 티커일 때
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
