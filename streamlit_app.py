import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="연령대별 독서량 분석", layout="wide")
st.title("📚 연령대별 독서량 분석 대시보드")

# ---------------------------------------
# 1) CSV 파일 업로드
# ---------------------------------------
uploaded = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded is not None:
    # CSV 읽기
    df = pd.read_csv(uploaded, encoding="latin1")

    # -----------------------------
    # 2) 전처리
    # -----------------------------
    df = df.rename(columns={df.columns[0]: "구분1", df.columns[1]: "연령대"})

    # 연령대만 추출
    age_df = df[df["구분1"].str.contains("연령", na=False)].copy()

    # Tidy 변환
    tidy = age_df.melt(
        id_vars="연령대",
        var_name="year",
        value_name="read_amount"
    )

    # 결측치 제거
    tidy = tidy[tidy["read_amount"] != "-"]

    # 숫자형 변환
    tidy["read_amount"] = tidy["read_amount"].astype(float)

    # -----------------------------
    # 3) 데이터 미리보기
    # -----------------------------
    st.subheader("데이터 미리보기")
    st.dataframe(tidy.head())

    # -----------------------------
    # 4) 연령대별 독서량 그래프
    # -----------------------------
    st.subheader("📈 연령대별 독서량 변화 추이")

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=tidy, x="year", y="read_amount", hue="연령대", marker="o")

    plt.title("연령대별 독서량 변화")
    plt.xlabel("연도")
    plt.ylabel("독서량")
    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(plt)

else:
    st.info("CSV 파일을 업로드하면 그래프가 생성됩니다.")

