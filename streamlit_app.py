import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="연령대별 독서량 분석", layout="wide")
st.title("📚 연령대별 독서량 분석 대시보드")

uploaded = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded is not None:
    # ⭐ 핵심 수정: 인코딩 cp949 사용 (한글 깨짐 해결)
    df = pd.read_csv(uploaded, encoding="cp949")

    df = df.rename(columns={df.columns[0]: "구분1", df.columns[1]: "연령대"})

    # "연령"이라는 글자를 담은 행만 선택
    age_df = df[df["구분1"].str.contains("연령", na=False)].copy()

    tidy = age_df.melt(
        id_vars="연령대",
        var_name="year",
        value_name="read_amount"
    )

    tidy = tidy[tidy["read_amount"] != "-"]
    tidy["read_amount"] = tidy["read_amount"].astype(float)

    st.subheader("데이터 미리보기")
    st.dataframe(tidy.head())

    st.subheader("📈 연령대별 독서량 변화 추이")

    chart = (
        alt.Chart(tidy)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:N", title="연도"),
            y=alt.Y("read_amount:Q", title="독서량"),
            color="연령대:N",
            tooltip=["연령대", "year", "read_amount"]
        )
        .properties(width=800, height=450)
    )

    st.altair_chart(chart, use_container_width=True)

else:
    st.info("CSV 파일을 업로드하면 그래프가 생성됩니다.")
