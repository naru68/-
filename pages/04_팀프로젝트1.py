import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(layout="wide")
st.title("🌍 국가별 전력 소비 예측 & 경제·인구 분석")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # 필요한 기본 컬럼
    base_cols = ["country", "year", "electricity_demand"]
    additional_cols = ["population", "gdp", "energy_per_capita", "energy_per_gdp"]
    all_required = base_cols + additional_cols

    if not all(col in df.columns for col in all_required):
        st.error(f"필요한 컬럼이 누락되었습니다. 다음 컬럼이 모두 있어야 합니다:\n{all_required}")
        st.stop()

    # 날짜 처리 및 전처리
    df = df[all_required].dropna()
    df["year"] = pd.to_datetime(df["year"], format="%Y")

    countries = df["country"].unique().tolist()
    selected_country = st.selectbox("국가를 선택하세요", countries)

    # 국가별 시계열 추출
    country_df = df[df["country"] == selected_country].copy()
    country_df.set_index("year", inplace=True)

    st.subheader(f"📈 {selected_country}의 전력 소비 예측 (ARIMA)")

    # ARIMA 예측
    ts = country_df["electricity_demand"]

    if len(ts) < 10:
        st.warning("⚠️ 예측을 위해 최소 10개 이상의 연도 데이터가 필요합니다.")
        st.stop()

    try:
        model = ARIMA(ts, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=10)

        last_year = ts.index.max().year
        forecast_years = pd.date_range(start=f'{last_year+1}', periods=10, freq='Y')
        forecast_series = pd.Series(forecast, index=forecast_years)

        fig, ax = plt.subplots(figsize=(12, 6))
        ts.plot(ax=ax, label="실제 전력 소비", color="blue")
        forecast_series.plot(ax=ax, label="예측 전력 소비 (10년)", color="red", linestyle="--")
        ax.set_ylabel("전력 소비량 (TWh)")
        ax.set_title(f"{selected_country} - 전력 소비 예측")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"모델 훈련 오류: {e}")

    # -----------------------
    # 📊 추가 분석 섹션
    # -----------------------
    st.subheader(f"📊 {selected_country}의 전력 소비 vs 인구 · 경제 지표")

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(country_df.index, country_df["electricity_demand"], label="전력 소비 (TWh)", color="blue", linewidth=2)
    ax2.plot(country_df.index, country_df["population"]/1e6, label="인구 (백만명)", linestyle="--", color="green")
    ax2.plot(country_df.index, country_df["gdp"]/1e3, label="GDP (단위: 천억)", linestyle="-.", color="orange")
    ax2.set_title(f"{selected_country} - 전력소비 vs 인구 & 경제")
    ax2.set_ylabel("값")
    ax2.legend()
    st.pyplot(fig2)

    st.markdown("**참고:** 단위 맞추기 위해 인구는 백만명, GDP는 천억 단위로 스케일링했습니다.")

    st.subheader("🧠 에너지 효율성 지표")
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    ax3.plot(country_df.index, country_df["energy_per_capita"], label="1인당 에너지 소비", color="purple")
    ax3.plot(country_df.index, country_df["energy_per_gdp"], label="GDP당 에너지 소비", color="red")
    ax3.set_title("에너지 효율성 추이")
    ax3.set_ylabel("에너지 단위")
    ax3.legend()
    st.pyplot(fig3)

else:
    st.info("CSV 파일을 업로드하면 예측 및 분석 결과가 표시됩니다.")
