import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(layout="wide")
st.title("🌍 국가별 전력 소비 예측 (ARIMA 기반)")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 필요한 컬럼만 선택
    required_columns = ["country", "year", "electricity_demand"]
    if not all(col in df.columns for col in required_columns):
        st.error(f"CSV 파일에 다음 컬럼이 모두 포함되어 있어야 합니다: {required_columns}")
        st.stop()

    # 숫자 타입 변환
    df = df[required_columns]
    df = df.dropna(subset=["electricity_demand"])
    df["year"] = pd.to_datetime(df["year"], format="%Y")

    countries = df["country"].unique().tolist()
    selected_country = st.selectbox("국가를 선택하세요", countries)

    # 해당 국가 데이터 추출
    country_df = df[df["country"] == selected_country].copy()
    country_df.set_index("year", inplace=True)
    ts = country_df["electricity_demand"]

    if len(ts) < 10:
        st.warning("⚠️ 예측을 위해 최소 10개 이상의 연도 데이터가 필요합니다.")
        st.stop()

    st.subheader(f"📈 {selected_country}의 전력 소비 예측 (10년)")

    try:
        # ARIMA 모델 훈련
        model = ARIMA(ts, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=10)

        last_year = ts.index.max().year
        forecast_years = pd.date_range(start=f'{last_year+1}', periods=10, freq='Y')
        forecast_series = pd.Series(forecast, index=forecast_years)

        # 시각화
        fig, ax = plt.subplots(figsize=(12, 6))
        ts.plot(ax=ax, label="실제 전력 소비", color="blue")
        forecast_series.plot(ax=ax, label="예측 전력 소비 (10년)", color="red", linestyle="--")
        ax.set_title(f"{selected_country}의 전력 소비 예측 (ARIMA)")
        ax.set_xlabel("연도")
        ax.set_ylabel("전력 소비량 (TWh 예상)")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"모델 훈련 중 오류 발생: {e}")
else:
    st.info("CSV 파일을 업로드하면 예측 결과가 표시됩니다.")
