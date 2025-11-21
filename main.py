# app.py
import streamlit as st
from textwrap import dedent

st.set_page_config(page_title="MBTI 진로 카운셀러 💼✨", page_icon="🧭", layout="centered")

# ---------- 스타일 ----------
st.markdown(
    dedent(
        """
        <style>
        .title {
            font-size:34px;
            font-weight:700;
            margin-bottom:6px;
        }
        .subtitle {
            color: #555;
            margin-top: -8px;
            margin-bottom: 18px;
        }
        .card {
            border-radius:12px;
            padding:16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            border: 1px solid rgba(0,0,0,0.04);
            background: linear-gradient(180deg, rgba(255,255,255,0.9), rgba(250,250,255,0.95));
            margin-bottom:12px;
        }
        .job-emoji { font-size:22px; margin-right:8px; }
        .job-title { font-weight:700; font-size:17px; display:inline-block; vertical-align:middle; }
        .job-desc { color:#444; margin-top:6px; font-size:13px; }
        .small { font-size:12px; color:#777; }
        </style>
        """),
    unsafe_allow_html=True,
)

# ---------- MBTI -> 추천 mapping ----------
MBTI_CAREERS = {
    "ISTJ": [("공인회계사/세무사", "체계적이고 규칙을 잘 따르는 업무에 강합니다. 📊"),
             ("공무원/사무관리", "안정성과 절차 중시 직무에 적합합니다. 🏛️"),
             ("프로젝트 매니저", "일정·자원 관리에 능합니다. 🧭")],
    "ISFJ": [("학교 행정/학생지도", "배려 깊은 지원 역할에 잘 맞습니다. 🧑‍🏫"),
             ("간호사/헬스케어 코디네이터", "세심한 돌봄이 강점입니다. 🩺"),
             ("박물관/아카이브 관리자", "전통·자료 보존을 잘 수행합니다. 🗃️")],
    "INFJ": [("상담사/임상심리사", "깊은 통찰과 진로상담에 강합니다. 🧠"),
             ("교육 컨설턴트", "개인 맞춤형 학습 설계에 적합합니다. 📝"),
             ("작가/콘텐츠 크리에이터", "의미를 전달하는 글쓰기에 적성있습니다. ✍️")],
    "INTJ": [("전략 컨설턴트", "시스템적 해결과 장기 계획에 강합니다. ♟️"),
             ("연구개발(R&D)", "이론적 분석·설계에 적합합니다. 🔬"),
             ("데이터 아키텍트/데이터 사이언티스트", "복잡한 구조를 설계합니다. 📈")],
    "ISTP": [("소프트웨어 엔지니어", "문제해결형 실무에 강합니다. 💻"),
             ("항공/기계 정비사", "도구·기술을 다루는 실무에 적합합니다. 🛠️"),
             ("긴급대응/소방관", "현장 판단력과 침착함이 빛납니다. 🚨")],
    "ISFP": [("디자이너(제품/그래픽)", "감성적인 시각 표현을 잘 합니다. 🎨"),
             ("영상·사진 작가", "미적 감각과 세세한 관찰에 강합니다. 📷"),
             ("동물·환경 관련 직무", "현장에서 섬세한 돌봄이 가능합니다. 🌱")],
    "INFP": [("심리치료/상담 분야", "가치 중심의 도움을 줄 수 있습니다. 💬"),
             ("출판/편집자", "문화·문학적 가치를 다루기 좋습니다. 📚"),
             ("NGO/비영리 기획", "이념과 가치를 실현하는 일에 적합합니다. 🤝")],
    "INTP": [("연구자(이공계/인문)", "이론 분석과 창의적 문제 해결에 강합니다. 🧩"),
             ("소프트웨어 아키텍트", "시스템적 설계에 재능이 있습니다. 🧠"),
             ("데이터 분석가/리서처", "호기심으로 깊게 파고듭니다. 🔍")],
    "ESTP": [("영업/비즈니스 개발", "즉각적 설득·상황대처에 강합니다. 🗣️"),
             ("이벤트 기획/PR", "현장 운영과 성과 창출에 적합합니다. 🎪"),
             ("증권 트레이더/마케팅", "스트레스 환경에서 성과를 냅니다. 📈")],
    "ESFP": [("연예/무대 예술가", "즉흥성과 표현력이 강점입니다. 🎤"),
             ("관광/서비스 업종", "사람을 즐겁게 하는 일을 잘합니다. 🧳"),
             ("패션/뷰티 관련 직무", "감각적 소비문화에 강합니다. 💄")],
    "ENFP": [("프랜차이즈 창업/스타트업", "아이디어 실행과 사람 연결을 좋아합니다. 🚀"),
             ("홍보/콘텐츠 기획", "창의적 스토리텔링에 적합합니다. ✨"),
             ("커리어 코치/강사", "사람 성장에 영감을 주는 역할이 맞습니다. 🌱")],
    "ENTP": [("스타트업 창업가", "새로운 기회 탐색과 토론을 즐깁니다. ⚡"),
             ("제품 매니저(PM)", "아이디어를 제품으로 연결시키는 역할에 강합니다. 🧭"),
             ("전략기획/혁신 컨설턴트", "논쟁과 전략 수립을 즐깁니다. ♻️")],
    "ESTJ": [("운영관리자/관리자직", "조직·절차를 세워 운영합니다. 🏢"),
             ("법률/검사", "규칙과 질서를 중시하는 역할에 적합합니다. ⚖️"),
             ("공급망/물류 관리자", "정확한 계획·집행에 강합니다. 🚚")],
    "ESFJ": [("교육자/학급 담당 교사", "타인 돌봄과 조직화에 탁월합니다. 🧑‍🏫"),
             ("인사(HR)/고객 서비스", "사람 중심 관리에 적합합니다. 🤝"),
             ("이벤트 코디네이터", "세심한 대인관계 운영을 잘합니다. 🎉")],
    "ENFJ": [("HR리더/조직개발", "사람의 성장과 팀워크를 이끄는 역할에 강합니다. 🌟"),
             ("정책·공공기관 리더", "사회적 영향력을 발휘할 수 있습니다. 🏛️"),
             ("컨텐츠·교육 기획자", "사람을 움직이는 메시지 제작에 적합합니다. 📣")],
    "ENTJ": [("CEO/기업 리더", "전략·실행을 이끄는 리더십이 뛰어납니다. 🦁"),
             ("경영 컨설턴트", "복잡한 문제를 구조적으로 해결합니다. 📊"),
             ("투자/벤처 캐피탈", "기회 식별과 자원 배분에 적합합니다. 💼")],
}

# ---------- UI ----------
st.markdown('<div class="title">MBTI 진로 카운셀러 💼✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">MBTI를 선택하면 그 유형에 어울리는 진로 3가지를 센스있게 추천해드립니다. 🎯</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("설정 🔧")
    st.markdown("아래에서 학생의 MBTI를 선택하세요.")
    mbti = st.selectbox(
        "학생의 MBTI",
        options=[""] + list(MBTI_CAREERS.keys()),
        index=0,
        help="예: ENFP, ISTJ 등"
    )
    st.markdown("---")
    st.markdown("원한다면 간단한 코멘트를 추가하세요:")
    note = st.text_input("학생에게 전달할 한 줄 코멘트", max_chars=120)
    if st.button("다시 추천받기 ✨"):
        st.experimental_rerun()

# ---------- 결과 보여주기 ----------
if not mbti:
    st.info("왼쪽 사이드바에서 MBTI를 선택하면 추천 진로가 표시됩니다. 🔽")
else:
    careers = MBTI_CAREERS.get(mbti, [])
    st.markdown(f"### 🔎 {mbti}의 추천 진로 3선")
    st.markdown(f'<div class="small">짧은 설명과 함께 바로 활용할 수 있는 아이디어를 제공합니다.</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (job, desc) in enumerate(careers):
        with cols[i]:
            st.markdown(f'<div class="card">', unsafe_allow_html=True)
            st.markdown(f'<div><span class="job-emoji">{"🔥" if i==0 else "⭐" if i==1 else "🌟"}</span>'
                        f'<span class="job-title">{job}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="job-desc">{desc}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 상담 메모(복사해서 사용하기)")
    default_note = f"추천: {mbti} → " + ", ".join([j for j, _ in careers])
    full_note = default_note + (f"  / 코멘트: {note}" if note else "")
    st.code(full_note, language=None)
    st.markdown("복사해서 학생에게 붙여넣기 해주시면 됩니다. ✉️")

    # 확장 정보
    with st.expander("💡 더 보기 — 각 진로에 대한 간단한 '초기 액션 플랜'"):
        for job, desc in careers:
            st.markdown(f"**{job}** — {desc}")
            st.markdown(f"- 시작 아이디어: {('인턴십/봉사 참여' if '현장' in desc or '돌봄' in desc else '단기 프로젝트·포트폴리오 만들기')}")
            st.markdown(f"- 추천 활동: {('현장 경험·실습' if '현장' in desc else '관련 동아리/공모전/온라인 코스 참여')}")
            st.markdown("")

# ---------- footer ----------
st.markdown("---")
st.markdown("Made with ❤️ by MBTI 진로 카운셀러 — 학생의 강점에 맞춘 간단한 출발점을 제공합니다. 필요하면 추천을 더 구체화해드릴게요! 🚀")
