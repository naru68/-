import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import plotly.express as px
from streamlit_plotly_events import plotly_events  # 추가

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

    # -----------------------
    # 🌍 지도 시각화 섹션 (Plotly) + 클릭 이벤트 처리
    # -----------------------
    st.subheader("🌍 세계 국가별 전력 소비량 지도")

    available_years = df["year"].dt.year.sort_values().unique()
    map_year = st.slider("지도로 볼 연도 선택", int(available_years.min()), int(available_years.max()), int(available_years.max()))

    map_df = df[df["year"].dt.year == map_year]
    map_fig = px.choropleth(map_df,
                            locations="country",
                            locationmode="country names",
                            color="electricity_demand",
                            color_continuous_scale="Blues",
                            title=f"{map_year}년 국가별 전력 소비량 (TWh)",
                            labels={"electricity_demand": "전력 소비량"})

    selected_points = plotly_events(map_fig, click_event=True, hover_event=False)
    
    if selected_points:
        # 클릭한 국가 이름 가져오기
        selected_country = selected_points[0]['location']

    else:
        selected_country = None

    # 기본 선택박스도 남겨둬서 직접 선택 가능
    if not selected_country:
        selected_country = st.selectbox("국가를 선택하세요", countries, index=0)
    else:
        st.write(f"지도에서 선택된 국가: **{selected_country}**")

    # -----------------------
    # 선택 국가 상세 분석 (기존 코드 대부분 재사용)
    # -----------------------
    country_df = df[df["country"] == selected_country].copy()
    country_df.set_index("year", inplace=True)

    st.subheader(f"📈 {selected_country}의 전력 소비 예측 (ARIMA)")

    ts = country_df["electricity_demand"]

    if len(ts) < 10:
        st.warning("⚠️ 예측을 위해 최소 10개 이상의 연도 데이터가 필요합니다.")
    else:
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

    st.subheader(f"📊 {selected_country}의 전력 소비 vs 인구 · 경제 지표")

    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(country_df.index, country_df["electricity_demand"], label="전력 소비 (TWh)", color="blue", linewidth=2)
    ax2.plot(country_df.index, country_df["population"]/1e6, label="인구 (백만명)", linestyle="--", color="green")
    ax2.plot(country_df.index, country_df["gdp"]/1e3, label="GDP (천억)", linestyle="-.", color="orange")
    ax2.set_title(f"{selected_country} - 전력소비 vs 인구 & 경제")
    ax2.set_ylabel("값")
    ax2.legend()
    st.pyplot(fig2)

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
