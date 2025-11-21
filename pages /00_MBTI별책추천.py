import streamlit as st
import random
import io

st.set_page_config(page_title="MBTI → 고전 추천 💡📚", layout="wide")

st.markdown("""
<style>
.card {background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.02));
            border-radius: 12px; padding:16px; box-shadow: 0 6px 18px rgba(0,0,0,0.12);}
.title {font-size:32px; font-weight:700}
.subtitle {color: #bdbdbd}
.badge {font-size:14px; padding:6px 10px; border-radius:999px; background: rgba(255,255,255,0.04)}
</style>
""", unsafe_allow_html=True)

# 앱 헤더
col1, col2 = st.columns([4,1])
with col1:
    st.markdown('<div class="title">당신의 MBTI에 딱 맞는 고전 책 추천 ✨</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">MBTI를 고르면 성향에 어울리는 고전 한 권을 센스 있게 골라드립니다.</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="badge">Made with ❤️ by Streamlit</div>', unsafe_allow_html=True)

st.write('')

# MBTI 목록
MBTIS = [
    'ISTJ','ISFJ','INFJ','INTJ',
    'ISTP','ISFP','INFP','INTP',
    'ESTP','ESFP','ENFP','ENTP',
    'ESTJ','ESFJ','ENFJ','ENTJ'
]

# 추천 데이터 (한글 설명 + 이모지)
RECOMMENDATIONS = {
    'ISTJ': {
        'title':'플라톤, 《국가 (The Republic)》',
        'emoji':'📏',
        'author':'Plato',
        'reason':'질서와 원칙을 중시하는 ISTJ에게 고전적 철학서로서 사회와 정의의 구조를 읽는 통찰을 줍니다.'
    },
    'ISFJ': {
        'title':'샬럿 브론테, 《제인 에어 (Jane Eyre)》',
        'emoji':'🕯️',
        'author':'Charlotte Brontë',
        'reason':'상대의 마음을 세심히 돌보는 ISFJ에게 인간관계와 책임감을 잔잔하게 다듬어주는 작품입니다.'
    },
    'INFJ': {
        'title':'겐지모노가타리, 《겐지 이야기 (The Tale of Genji)》',
        'emoji':'🍃',
        'author':'Murasaki Shikibu',
        'reason':'내면의 깊이를 탐구하는 INFJ에게 섬세한 심리 묘사와 인간 드라마가 큰 울림을 줍니다.'
    },
    'INTJ': {
        'title':'마르쿠스 아우렐리우스, 《명상록 (Meditations)》',
        'emoji':'🧭',
        'author':'Marcus Aurelius',
        'reason':'전략적 사고와 자기성찰을 좋아하는 INTJ에게 실용적인 철학적 통찰을 선사합니다.'
    },
    'ISTP': {
        'title':'허먼 멜빌, 《모비 딕 (Moby-Dick)》',
        'emoji':'⚓',
        'author':'Herman Melville',
        'reason':'행동 중심의 ISTP에게 모험과 기술적 디테일, 인간과 자연의 대결이 흥미를 돋웁니다.'
    },
    'ISFP': {
        'title':'헨리 데이비드 소로, 《월든 (Walden)》',
        'emoji':'🌿',
        'author':'Henry David Thoreau',
        'reason':'감성적이고 예술적인 ISFP에게 자연과 단순한 삶을 통해 영감을 주는 에세이입니다.'
    },
    'INFP': {
        'title':'앙투안 드 생텍쥐페리, 《어린 왕자 (The Little Prince)》',
        'emoji':'🌟',
        'author':'Antoine de Saint-Exupéry',
        'reason':'이상주의적 INFP에게 순수한 상징과 은유로 마음을 건드리는 작품입니다.'
    },
    'INTP': {
        'title':'조너선 스위프트, 《걸리버 여행기 (Gulliver\'s Travels)》',
        'emoji':'🧪',
        'author':'Jonathan Swift',
        'reason':'논리와 아이디어를 즐기는 INTP에게 풍자와 사유의 장을 제공하는 고전입니다.'
    },
    'ESTP': {
        'title':'오승일 외, 《서유기 (Journey to the West)》',
        'emoji':'🔥',
        'author':'Wu Cheng\'en (traditional)',
        'reason':'모험을 즐기는 ESTP에게 액션과 빠른 전개, 유머가 가득한 서사입니다.'
    },
    'ESFP': {
        'title':'윌리엄 셰익스피어, 《한여름 밤의 꿈 (A Midsummer Night\'s Dream)》',
        'emoji':'🎭',
        'author':'William Shakespeare',
        'reason':'사교적이고 즉흥적인 ESFP에게 유쾌한 로맨스와 환상이 잘 맞습니다.'
    },
    'ENFP': {
        'title':'루이스 캐럴, 《이상한 나라의 앨리스 (Alice\'s Adventures in Wonderland)》',
        'emoji':'🌀',
        'author':'Lewis Carroll',
        'reason':'상상력이 풍부한 ENFP에게 기발하고 창의적인 세계관이 즐거움을 줍니다.'
    },
    'ENTP': {
        'title':'미겔 데 세르반테스, 《돈키호테 (Don Quixote)》',
        'emoji':'🤺',
        'author':'Miguel de Cervantes',
        'reason':'논쟁과 아이디어를 즐기는 ENTP에게 유머와 풍자, 끝없는 질문거리를 던집니다.'
    },
    'ESTJ': {
        'title':'레프 톨스토이, 《전쟁과 평화 (War and Peace)》',
        'emoji':'🏛️',
        'author':'Leo Tolstoy',
        'reason':'책임감 있고 조직적인 ESTJ에게 방대한 역사와 지도력, 인간 군상의 교훈을 제공합니다.'
    },
    'ESFJ': {
        'title':'제인 오스틴, 《오만과 편견 (Pride and Prejudice)》',
        'emoji':'💌',
        'author':'Jane Austen',
        'reason':'관계를 중요시하는 ESFJ에게 사회적 관습과 인간관계의 섬세함을 선사합니다.'
    },
    'ENFJ': {
        'title':'빅토르 위고, 《레 미제라블 (Les Misérables)》',
        'emoji':'🔥',
        'author':'Victor Hugo',
        'reason':'타인을 이끄는 ENFJ에게 사회 정의와 깊은 공감을 불러일으키는 작품입니다.'
    },
    'ENTJ': {
        'title':'니콜로 마키아벨리, 《군주론 (The Prince)》',
        'emoji':'♟️',
        'author':'Niccolò Machiavelli',
        'reason':'결단력 있는 ENTJ에게 권력과 전략에 관한 냉철한 통찰을 제공합니다.'
    }
}

# 사이드바에서 MBTI 선택
st.sidebar.title('MBTI 선택 🧭')
selected = st.sidebar.selectbox('당신(또는 학생)의 MBTI를 골라주세요:', MBTIS, index=0)

# 랜덤 추천 버튼
if st.sidebar.button('랜덤 추천 🎲'):
    selected = random.choice(MBTIS)

# 메인 카드
rec = RECOMMENDATIONS[selected]

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2 = st.columns([3,1])
    with c1:
        st.markdown(f"### {rec['emoji']} {rec['title']}")
        st.write(f"**저자:** {rec['author']}")
        st.write(rec['reason'])
        with st.expander('추천 이유 자세히 보기 🔍'):
            st.write(rec['reason'])
            st.write('\n한 줄 요약: 이 책은 당신의 성향에 맞는 주제와 서사를 제공합니다.')
    with c2:
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.download_button('추천 내역 다운로드 ⤓', data=io.StringIO(f"MBTI: {selected}\n책: {rec['title']}\n저자: {rec['author']}\n이유: {rec['reason']}"), file_name='mbti_recommendation.txt')
    st.markdown('</div>', unsafe_allow_html=True)

# 추가 기능: 여러 유형 비교
st.write('')
st.markdown('---')
st.write('다른 유형과 비교해 보고 싶나요? 아래에서 최대 3개를 선택하세요. 👇')
choices = st.multiselect('비교할 MBTI (최대 3개)', MBTIS, default=[selected])
if len(choices) > 3:
    st.warning('최대 3개만 선택할 수 있습니다.')

if choices:
    cols = st.columns(len(choices))
    for i, mb in enumerate(choices):
        with cols[i]:
            r = RECOMMENDATIONS[mb]
            st.markdown(f"### {r['emoji']} {r['title']}")
            st.write(f"**저자:** {r['author']}")
            st.write(r['reason'])

# 푸터
st.markdown('---')
st.markdown('**Tip:** 스트림릿 클라우드에 배포하려면 이 파일을 GitHub 저장소에 올리고 Streamlit으로 연결하세요. 🚀')
