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

    # 첫 번째 열을 인덱스로 설정 (국가명), 연도별 데이터로 전환
    df = df.set_index(df.columns[0])
    df = df.transpose()

    # "year"라는 값이 행으로 들어가 있으면 제거
    df = df[df.index != "year"]

    # 인덱스 → datetime 처리
    try:
        df.index.name = "Year"
        df.reset_index(inplace=True)
        df['Year'] = pd.to_datetime(df['Year'], format='%Y')
        df.set_index('Year', inplace=True)
    except Exception as e:
        st.error(f"'Year' 열을 날짜로 변환할 수 없습니다: {e}")
        st.stop()

    # 숫자형 국가만 필터링
    countries = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
    if not countries:
        st.error("예측 가능한 숫자형 국가 데이터가 없습니다.")
        st.stop()

    selected_country = st.selectbox("국가 또는 지역을 선택하세요", countries)

    ts = df[selected_country].dropna()

    if len(ts) < 15:
        st.warning("⚠️ 예측하기에 데이터가 너무 적습니다. 최소 15개 이상 필요합니다.")
        st.stop()

    st.subheader(f"📈 {selected_country}의 전력 소비 예측 (10년)")

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
