import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px

st.set_page_config(layout="wide")
st.title("🌍 국가별 전력 소비 예측 & 경제·인구 분석 + 지도 시각화")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    base_cols = ["country", "year", "electricity_demand"]
    additional_cols = ["population", "gdp", "energy_per_capita", "energy_per_gdp"]
    all_required = base_cols + additional_cols

    if not all(col in df.columns for col in all_required):
        st.error(f"필요한 컬럼이 누락되었습니다. 다음 컬럼이 모두 있어야 합니다:\n{all_required}")
        st.stop()

    df = df[all_required].dropna()
    df = df[df["year"].apply(lambda x: str(x).isnumeric())]
    df["year"] = pd.to_datetime(df["year"], format="%Y")

    countries = df["country"].unique().tolist()
    selected_countries = st.multiselect("국가(들)를 선택하세요 (최대 3개)", countries, default=countries[:1])

    if not selected_countries:
        st.warning("최소 한 개 이상의 국가를 선택하세요.")
        st.stop()

    if len(selected_countries) > 3:
        st.warning("최대 3개 국가까지만 선택 가능합니다.")
        st.stop()

    st.subheader(f"📈 선택한 국가들의 전력 소비 예측 비교 (ARIMA)")

    fig, ax = plt.subplots(figsize=(14, 7))

    colors = ["blue", "green", "red"]  # 최대 3개 국가용 색상

    for i, country in enumerate(selected_countries):
        country_df = df[df["country"] == country].copy()
        country_df.set_index("year", inplace=True)
        ts = country_df["electricity_demand"]

        if len(ts) < 10:
            st.warning(f"⚠️ {country}의 데이터가 10년 미만으로 예측을 할 수 없습니다.")
            continue

        # 실제값 그리기
        ax.plot(ts.index, ts.values, label=f"{country} 실제", color=colors[i], linewidth=2)

        # ARIMA 예측
        try:
            model = ARIMA(ts, order=(1, 1, 1))
            model_fit = model.fit()
            forecast = model_fit.forecast(steps=10)

            last_year = ts.index.max().year
            forecast_years = pd.date_range(start=f'{last_year+1}', periods=10, freq='Y')
            forecast_series = pd.Series(forecast, index=forecast_years)

            ax.plot(forecast_series.index, forecast_series.values,
                    label=f"{country} 예측 (10년)", color=colors[i], linestyle="--")
        except Exception as e:
            st.error(f"{country} 모델 훈련 오류: {e}")

    ax.set_ylabel("전력 소비량 (TWh)")
    ax.set_title("선택 국가별 전력 소비 실제값 및 10년 예측 비교")
    ax.legend()
    st.pyplot(fig)

    # 나머지 분석 및 지도 시각화는 기존 코드와 동일하게 넣으면 됩니다.
    # (원하면 전체 코드 이어서 제공 가능)

else:
    st.info("CSV 파일을 업로드하면 예측 및 분석 결과가 표시됩니다.")
