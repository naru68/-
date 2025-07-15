import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA

st.set_page_config(layout="wide")
st.title("🌍 세계 전력 소비 예측 웹앱")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    # CSV 불러오기
    df = pd.read_csv(uploaded_file)

    # 첫 번째 열 이름을 'Year'로 강제 지정 (예: 'Unnamed: 0' → 'Year')
    df.rename(columns={df.columns[0]: 'Year'}, inplace=True)

    # 열 이름 보여주기
    st.subheader("🧾 데이터 열 이름")
    st.write(df.columns.tolist())

    # 상위 10행 미리보기
    st.subheader("📊 데이터 미리보기 (상위 10행)")
    st.dataframe(df.head(10))

    # 전체 데이터 보기
    if st.checkbox("🔍 전체 데이터 보기"):
        st.subheader("📋 전체 데이터")
        st.dataframe(df)

    # 연도 전처리
    try:
        df['Year'] = pd.to_datetime(df['Year'], format='%Y')
        df.set_index('Year', inplace=True)
    except Exception as e:
        st.error(f"'Year' 컬럼을 날짜로 변환할 수 없습니다: {e}")
        st.stop()

    # 국가 선택
    countries = [col for col in df.columns if df[col].dtype in ['float64', 'int64']]
    if not countries:
        st.error("예측할 수 있는 숫자형 컬럼이 없습니다.")
        st.stop()

    selected_country = st.selectbox("국가 또는 지역을 선택하세요", countries)

    # 시계열 데이터 추출
    ts = df[selected_country].dropna()

    if len(ts) < 15:
        st.warning("⚠️ 데이터가 너무 적습니다. 최소 15개 이상 필요합니다.")
        st.stop()

    st.subheader(f"📈 {selected_country}의 전력 소비 예측 (ARIMA 기반)")

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
        ax.set_ylabel("전력 소비")
        ax.set_xlabel("연도")
        ax.set_title(f"{selected_country} - 전력 소비 예측")
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"모델 학습 또는 예측 중 오류 발생: {e}")

else:
    st.info("왼쪽 상단의 사이드바 또는 위에서 CSV 파일을 업로드해 주세요.")
