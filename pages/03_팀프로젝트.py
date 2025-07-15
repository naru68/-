import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

st.title("🌍 국가별 전력 소비 예측 (ARIMA, 10년)")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'Year' not in df.columns:
        st.error("⚠️ 'Year'라는 컬럼이 필요합니다.")
        st.stop()

    # 연도 변환
    df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    df.set_index('Year', inplace=True)

    countries = [col for col in df.columns]
    selected_country = st.selectbox("국가를 선택하세요", countries)

    ts = df[selected_country].dropna()

    if len(ts) < 15:
        st.warning("⚠️ 데이터가 너무 적습니다. 최소 15개 이상 필요합니다.")
        st.stop()

    st.subheader(f"📈 {selected_country}의 전력 소비 예측")

    # ARIMA 모델 (간단히 (1,1,1)로 지정)
    try:
        model = ARIMA(ts, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=10)

        last_year = ts.index.max().year
        future_years = pd.date_range(start=f'{last_year+1}', periods=10, freq='Y')
        forecast_series = pd.Series(forecast, index=future_years)

        fig, ax = plt.subplots(figsize=(10, 5))
        ts.plot(ax=ax, label="실제 데이터", color='blue')
        forecast_series.plot(ax=ax, label="예측 (10년)", color='red', linestyle='--')
        ax.set_ylabel("전력 소비")
        ax.set_xlabel("연도")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"모델 학습 오류: {e}")
else:
    st.info("CSV 파일을 업로드하면 예측 결과를 볼 수 있습니다.")
