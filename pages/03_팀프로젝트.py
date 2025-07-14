import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pmdarima import auto_arima

# 파일 업로드 or 기본 데이터 불러오기
st.title("🌍 국가별 전력 소비 예측 (10년)")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    
    # 간단한 전처리 (연도형 변환)
    if 'Year' in df.columns:
        df['Year'] = pd.to_datetime(df['Year'], format='%Y')
    else:
        st.error("⚠️ 'Year'라는 컬럼이 필요합니다.")
        st.stop()

    # 국가 컬럼 목록 추출 (예: Country, 또는 State 등)
    country_col = [col for col in df.columns if col.lower() not in ['year']]
    
    selected_country = st.selectbox("국가를 선택하세요", country_col)

    # 시계열 데이터 준비
    ts_data = df[['Year', selected_country]].dropna()
    ts_data.set_index('Year', inplace=True)

    # 모델 학습 및 예측
    st.subheader(f"📈 {selected_country}의 전력 소비 추이 및 예측")
    
    try:
        model = auto_arima(ts_data, seasonal=False, trace=False)
        forecast = model.predict(n_periods=10)

        # 연도 생성
        last_year = ts_data.index.max().year
        future_years = pd.date_range(start=f'{last_year+1}', periods=10, freq='Y')
        forecast_df = pd.Series(forecast, index=future_years)

        # 시각화
        fig, ax = plt.subplots(figsize=(10, 5))
        ts_data.plot(ax=ax, label="실제 데이터", color='blue')
        forecast_df.plot(ax=ax, label="예측 (10년)", color='red', linestyle='--')
        ax.set_ylabel("전력 소비량")
        ax.set_xlabel("연도")
        ax.legend()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"모델 학습 중 오류 발생: {e}")
else:
    st.info("CSV 파일을 업로드하면 결과를 볼 수 있습니다.")
