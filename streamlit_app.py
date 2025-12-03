import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="연령대별 독서량 분석", layout="wide")
st.title("📚 연령대별 독서량 분석 (2025년 기준)")

uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is None:
    st.info("CSV 파일을 업로드하면 분석을 시작할 수 있어요.")
    st.stop()

# 1. CSV 로드
df = pd.read_csv(uploaded_file, encoding="utf-8", engine="python")

# 2. 연령대 행만 필터
age_df = df[(df["특성별(1)"] == "연령")].copy()

# 3. 컬럼명 확인
st.subheader("데이터 미리보기")
st.dataframe(age_df.head(), use_container_width=True)

# 핵심 컬럼 정리
# 총독서량 = "2025"
# 독서인구 1인당 평균 독서권수 = "2025.1"
# 종이책 = "2025.2"
# 전자책 = "2025.3"

# -----------------------
# 탭 구성
# -----------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "총독서량 비교",
    "종이책·전자책 비교",
    "세부 항목 히트맵",
    "연령대별 상세 보기"
])

# -----------------------
# 1) 총독서량 비교
# -----------------------
with tab1:
    st.header("📌 연령대별 총독서량 비교 (2025)")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(
        data=age_df,
        x="특성별(2)",
        y="2025",
        ax=ax
    )
    ax.set_ylabel("총 독서량")
    ax.set_xlabel("연령대")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# -----------------------
# 2) 종이책·전자책 비교
# -----------------------
with tab2:
    st.header("📌 종이책 vs 전자책 독서량 비교 (2025)")
    
    melted = age_df.melt(
        id_vars="특성별(2)",
        value_vars=["2025.2", "2025.3"],
        var_name="type",
        value_name="amount"
    )

    type_map = {
        "2025.2": "종이책",
        "2025.3": "전자책"
    }
    melted["type"] = melted["type"].map(type_map)

    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(
        data=melted,
        x="특성별(2)",
        y="amount",
        hue="type",
        ax=ax
    )
    ax.set_xlabel("연령대")
    ax.set_ylabel("독서량")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# -----------------------
# 3) 히트맵 분석
# -----------------------
with tab3:
    st.header("📌 연령대 × 독서 항목 히트맵")

    # 숫자형 컬럼만 선택
    num_cols = [col for col in age_df.columns if "2025" in col]

    heat_df = age_df.set_index("특성별(2)")[num_cols]

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(heat_df, annot=True, fmt=".1f", cmap="Blues")
    st.pyplot(fig)

# -----------------------
# 4) 특정 연령대 상세 보기
# -----------------------
with tab4:
    st.header("📌 연령대별 상세 보기")

    selected_age = st.selectbox("연령대를 선택하세요", age_df["특성별(2)"].unique())

    detail = age_df[age_df["특성별(2)"] == selected_age].T
    st.subheader(f"▶ {selected_age} 상세 데이터")
    st.dataframe(detail, use_container_width=True)
