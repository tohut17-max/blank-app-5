import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="연령대별 독서량 분석", layout="wide")
st.title("📚 연령대별 독서량 분석 대시보드")

# ---------------------------------------
# 1) 파일 업로드
# ---------------------------------------
uploaded = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded is not None:
    df = pd.read_csv(uploaded, encoding="utf-8")

    # 컬럼명 정리
    df = df.rename(columns={df.columns[0]: "구분1", df.columns[1]: "연령대"})

    # 연령대만 선택
    age_df = df[df["구분1"].str.contains("연령", na=False)].copy()

    # Tidy 변환
    tidy = age_df.melt(
        id_vars="연령대",
        var_name="year",
        value_name="read_amount"
    )

    tidy = tidy[tidy["read_amount"] != "-"]
    tidy["read_amount"] = tidy["read_amount"].astype(float)

    # ---------------------------------------
    # 2) 사이드바 필터 UI
    # ---------------------------------------
    st.sidebar.header("🔎 데이터 필터")

    # 연도 리스트
    years = sorted(tidy["year"].unique())

    # 연도 멀티 선택
    selected_years = st.sidebar.multiselect(
        "연도 선택",
        options=years,
        default=years  # 기본값: 전체 연도
    )

    # 연령대 리스트
    age_groups = sorted(tidy["연령대"].unique())

    selected_ages = st.sidebar.multiselect(
        "연령대 선택",
        options=age_groups,
        default=age_groups  # 기본값: 전체 연령대
    )

    # 필터 적용
    filtered = tidy[
        tidy["year"].isin(selected_years) &
        tidy["연령대"].isin(selected_ages)
    ]

    # ---------------------------------------
    # 3) 데이터 미리보기
    # ---------------------------------------
    st.subheader("🔍 필터링된 데이터 미리보기")
    st.dataframe(filtered)

    # ---------------------------------------
    # 4) Altair 라인 차트 (인터랙티브)
    # ---------------------------------------
    st.subheader("📈 연령대별 독서량 변화 추이")

    chart = (
        alt.Chart(filtered)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:N", title="연도"),
            y=alt.Y("read_amount:Q", title="독서량"),
            color="연령대:N",
            tooltip=["연령대", "year", "read_amount"]
        )
        .properties(width=900, height=450)
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

else:
    st.info("CSV 파일을 업로드하면 그래프가 생성됩니다.")
