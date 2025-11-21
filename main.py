# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

DATA_PATH = "/mnt/data/countriesMBTI_16types.csv"

st.set_page_config(page_title="MBTI by Country 🌏", layout="wide")

st.title("MBTI 분포 — 나라별 상위/하위 10선 📊")
st.caption("MBTI를 선택하면 해당 유형의 비율이 높은 나라 / 낮은 나라를 각각 보여줍니다. (Plotly로 interactive)")

@st.cache_data
def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    # 컬럼 정리: MBTI 컬럼들이 있는지 확인
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# MBTI 목록 자동 생성 (Country 컬럼 제외)
mbti_cols = [c for c in df.columns if c.lower() != "country"]
mbti_cols_sorted = sorted(mbti_cols)

col1, col2 = st.columns([2,1])
with col1:
    chosen_mbti = st.selectbox("MBTI 유형을 선택하세요:", mbti_cols_sorted, index=mbti_cols_sorted.index("INFJ") if "INFJ" in mbti_cols_sorted else 0)
with col2:
    show_table = st.checkbox("상세 테이블 보기", value=False)

# 안전 검사
if chosen_mbti not in df.columns:
    st.error(f"선택한 MBTI ({chosen_mbti}) 컬럼을 찾을 수 없습니다.")
    st.stop()

# 정렬해서 상위/하위 10개 추출
series = df[["Country", chosen_mbti]].copy()
series = series.rename(columns={chosen_mbti: "ratio"})
series_sorted = series.sort_values(by="ratio", ascending=False)

top10 = series_sorted.head(10)
bottom10 = series_sorted.tail(10).sort_values(by="ratio", ascending=True)

# Plotly bar charts
def plot_bar(dataframe, title):
    fig = px.bar(
        dataframe,
        x="ratio",
        y="Country",
        orientation="h",
        hover_data={"ratio":":.4f"},
        text="ratio",
    )
    fig.update_traces(texttemplate="%{text:.4f}", textposition="outside")
    fig.update_layout(
        title=title,
        yaxis={"categoryorder":"total ascending"},
        margin=dict(l=150, r=40, t=60, b=40),
        height=420,
    )
    return fig

st.markdown("### 상위 10개 국가 — 비율 높은 순 🥇")
fig_top = plot_bar(top10.sort_values(by="ratio", ascending=True), f"Top 10 countries for {chosen_mbti}")
st.plotly_chart(fig_top, use_container_width=True)

st.markdown("### 하위 10개 국가 — 비율 낮은 순 🥈")
fig_bottom = plot_bar(bottom10, f"Bottom 10 countries for {chosen_mbti}")
st.plotly_chart(fig_bottom, use_container_width=True)

if show_table:
    st.markdown("#### 전체 국가 비율 (내림차순)")
    st.dataframe(series_sorted.reset_index(drop=True).style.format({"ratio":"{:.4f}"}))

# ----- MBTI별 책추천 섹션 (수정 및 즉시 동작) -----
st.markdown("---")
st.header("MBTI별 고전 책 추천 📚")

# MBTI -> 추천 도서 매핑 (고전 위주 예시)
MBTI_BOOKS = {
    "INFJ": ["빅토르 위고, 《레 미제라블》", "알베르 까뮈, 《이방인》", "요한 볼프강 폰 괴테, 《젊은 베르테르의 슬픔》"],
    "ISFJ": ["루이자 메이 올컷, 《작은 아씨들》", "도스토예프스키, 《백치》", "제인 오스틴, 《오만과 편견》"],
    "INTP": ["플라톤, 《국가》", "루트비히 비트겐슈타인, 《논리·철학적 논고》 (발췌)", "오노레 드 발자크, 《고리오 영감》"],
    "ISFP": ["나쓰메 소세키, 《마음》", "에밀리 브론테, 《폭풍의 언덕》", "이상, 《날개》"],
    "ENTP": ["조지 오웰, 《1984》", "토마스 페인, 《상식》 (발췌)", "카를 마르크스 & 엥겔스, 《공산당 선언》 (발췌)"],
    "INFP": ["한나 아렌트, 《예루살렘의 아이히만》", "가브리엘 가르시아 마르케스, 《백년의 고독》", "프란츠 카프카, 《변신》"],
    "ENTJ": ["니체, 《차라투스트라는 이렇게 말했다》", "마키아벨리, 《군주론》", "토크빌, 《미국의 민주주의》"],
    "ISTP": ["어니스트 헤밍웨이, 《노인과 바다》", "에드가 앨런 포, 《어셔가의 몰락》", "허먼 멜빌, 《모비 딕》 (발췌)"],
    "INTJ": ["아서 코난 도일, 《셜록 홈즈 전집》", "아리스토텔레스, 《정치학》 (발췌)", "아담 스미스, 《국부론》 (발췌)"],
    "ESFP": ["루이스 캐럴, 《이상한 나라의 앨리스》", "오스카 와일드, 《도리언 그레이의 초상》", "마크 트웨인, 《허클베리 핀의 모험》"],
    "ENFP": ["빅토르 프랭클, 《죽음의 수용소에서》", "알베르트 카뮈, 《전락》", "로맹 롤랑, 《장크리스트프》 (발췌)"],
    "ESTP": ["잭 런던, 《야성의 부름》", "러디어드 키플링, 《정글북》", "J.D. 샐린저, 《호밀밭의 파수꾼》"],
    "ISTJ": ["찰스 디킨스, 《두 도시 이야기》", "밀턴, 《실낙원》 (발췌)", "호메로스, 《일리아스》 (발췌)"],
    "ENFJ": ["톨스토이, 《안나 카레니나》", "헨리크 입센, 《인형의 집》", "에밀 졸라, 《테레즈 라캥》"],
    "ESFJ": ["찰스 페로, 《동화 모음》", "샬롯 브론테, 《제인 에어》", "소포클레스, 《오이디푸스 왕》 (발췌)"],
    "ESTJ": ["토머스 칼라일, 《영웅 숭배론》", "시몬 드 보부아르, 《제2의 성》 (발췌)", "플루타르코스, 《영웅전》 (발췌)"],
}

books = MBTI_BOOKS.get(chosen_mbti, ["추천 도서가 등록되어 있지 않습니다."])
st.markdown(f"**선택한 MBTI: {chosen_mbti}**")
for i, b in enumerate(books, start=1):
    st.write(f"{i}. {b}")

st.caption("원하시면 각 도서에 대한 간략 소개나 수업 아이디어(활동지, 토론 질문 등)를 바로 생성해 드릴게요. 📚✨")
