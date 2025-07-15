import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(layout="wide")
st.title("🌍 세계 전력 소비 예측 웹앱 (ARIMA 기반)")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    # 데이터 읽기
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 원본 데이터 미리보기")
    st.dataframe(df.head(10))

    # 첫 번째 열이 국가 이름, 나머지는 연도로 간주
    df = df.set_index(df.columns[0])  # 국가명을 인덱스로
    df = df.transpose()  # 연도-국가 시계열 구조로 변환

    # 열 이름 정리
    df.index.name = "Year"
    df.reset_index(inplace=True)

    # 연도 컬럼 처리
    try:
        df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    except Exception as e:
        st.error(f"'Year' 열을 날짜로 변환할 수 없습니다: {e}")
        st.stop()

    df.set_index('Year', inplace=True)

    # 숫자형 컬럼(국가) 목록
    countries = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
    if not countries:
        st.error("숫자형 국가 데이터가 없습니다.")
        st.stop()

    # 국가 선택
    selected_country = st.selectbox("국가 또는 지역을 선택하세요", countries)

    # 시계열 추출
    ts = df[selected_country].dropna()

    if len(ts) < 15:
        st.warning("⚠️ 예측하기에 데이터가 너무 적습니다 (15개 이상 필요).")
        st.stop()

    st.subheader(f"📈 {selected_country}의 전력 소비 예측 (10년)")

    # ARIMA 모델 훈련 및 예측
    try:
        model = ARIMA(ts, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=10)

        last_year = ts.index.max().year
        future_years = pd.date_range(start=f'{last_year+1}', periods=10, freq='Y')
        forecast_series = pd.Series(forecast, index=future_years)

        # 시각화
        fig, ax = plt.subplots(figsize=(12, 6))
        ts.plot(ax=ax, label="실제 데이터", color='blue')
        forecast_series.plot(ax=ax, label="예측 (10년)", color='red', linestyle='--')
        ax.set_ylabel("전력 소비량")
        ax.set_xlabel("연도")
        ax.set_title(f"{selected_country} - 전력 소비 예측")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"모델 학습 오류: {e}")
else:
    st.info("CSV 파일을 업로드하면 예측을 시작할 수 있습니다.")
