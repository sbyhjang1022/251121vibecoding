# app.py
import streamlit as st
import pandas as pd
import altair as alt

# 페이지 설정
st.set_page_config(page_title="MBTI by Country 🌍", layout="centered")

st.title("MBTI 비율 상/하위 국가 보기 🌐")

# 데이터 로드 (같은 폴더에 있는 CSV 경로 사용)
DATA_PATH = "countriesMBTI_16types.csv"

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # 확실히 Country 컬럼이 문자열이고 나머지는 숫자인지 확인
    df['Country'] = df['Country'].astype(str)
    for c in df.columns:
        if c != 'Country':
            df[c] = pd.to_numeric(df[c], errors='coerce')
    return df

df = load_data(DATA_PATH)

# MBTI 타입 선택 UI
mbti_types = [c for c in df.columns if c != 'Country']
default = "INFJ" if "INFJ" in mbti_types else mbti_types[0]
mbti_choice = st.selectbox("MBTI 유형을 선택하세요:", mbti_types, index=mbti_types.index(default))

# 정렬해서 상위 10 / 하위 10 준비
df_sorted = df[['Country', mbti_choice]].sort_values(by=mbti_choice, ascending=False).reset_index(drop=True)
top10 = df_sorted.head(10).copy()
bottom10 = df_sorted.tail(10).copy().sort_values(by=mbti_choice, ascending=True)

# 숫자 컬럼 이름 통일 (altair에서 쓰기 편함)
top10 = top10.rename(columns={mbti_choice: "value"})
bottom10 = bottom10.rename(columns={mbti_choice: "value"})

# 선택(클릭) 및 호버 셀렉션 정의
click = alt.selection_single(fields=['Country'], on='click', empty='none')
hover = alt.selection_single(fields=['Country'], on='mouseover', nearest=True, empty='none')

def make_bar_chart(data, title, ascending=False):
    # y 순서 지정: 그래프에서 가장 큰값이 위에 오도록 (가독성)
    data = data.copy()
    data['Country'] = pd.Categorical(data['Country'], categories=list(data['Country']), ordered=True)

    base = alt.Chart(data).mark_bar().encode(
        x=alt.X('value:Q', title='비율'),
        y=alt.Y('Country:N', sort=None, title=None),
        tooltip=[alt.Tooltip('Country:N', title='국가'), alt.Tooltip('value:Q', title='비율', format='.4f')],
        color=alt.condition(click | hover, alt.value('#4C78A8'), alt.value('#9FB0D3'))
    ).properties(
        title=title,
        width=700,
        height=300
    ).add_selection(
        click, hover
    )

    # 텍스트 라벨 (값)
    text = alt.Chart(data).mark_text(align='left', dx=3, dy=0).encode(
        y=alt.Y('Country:N', sort=None),
        x=alt.X('value:Q'),
        text=alt.Text('value:Q', format='.4f')
    )

    chart = (base + text).configure_title(fontSize=16, anchor='start')
    return chart

st.subheader(f"선택: {mbti_choice}  — 상위 10개 국가")
st.altair_chart(make_bar_chart(top10, title=f"Top 10 countries for {mbti_choice}"), use_container_width=False)

st.subheader(f"{mbti_choice} 비율이 가장 낮은 10개 국가")
st.altair_chart(make_bar_chart(bottom10, title=f"Bottom 10 countries for {mbti_choice}"), use_container_width=False)

# 추가 정보 패널
st.markdown("---")
st.markdown(
    "사용법: 국가 막대를 **마우스로 올리면(hover)** 강조되고, **클릭하면(click)** 해당 국가가 색으로 표시됩니다. "
    "툴팁에서 정확한 비율을 확인하세요."
)

# 데이터 다운로드 버튼 (원본 CSV)
with open(DATA_PATH, "rb") as f:
    csv_bytes = f.read()
st.download_button("원본 CSV 다운로드", data=csv_bytes, file_name="countriesMBTI_16types.csv", mime="text/csv")
