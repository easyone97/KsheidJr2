import streamlit as st
import pandas as pd
import plotly.express as px
import time
import os
from streamlit_option_menu import option_menu

# 페이지 설정
st.set_page_config(page_title="Descriptive Analytics", page_icon="🌎", layout="wide")

# CSS 스타일 로드
css_file = 'style.css'
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    st.write("CSS 파일을 찾을 수 없습니다. 기본 스타일을 사용합니다.")

# CSV 파일 로드
csv_file = 'Downloadfile/final_result_test.csv'
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
else:
    st.write("CSV 파일을 찾을 수 없습니다. 기본 데이터셋을 사용합니다.")
    # 기본 데이터셋 생성
    data = {
        'number': [1, 2, 3],
        '혼합된질문': ['질문1', '질문2', '질문3'],
        '답변': ['답변1', '답변2', '답변3'],
        'type': ['Type1', 'Type2', 'Type3'],
        '탈옥성공여부': ['success', 'fail', 'success']
    }
    df = pd.DataFrame(data)

# 함수 정의

def HomePage():
    # 데이터프레임 출력
    with st.expander("🧭 My database"):
        shwdata = st.multiselect('Filter:', df.columns, default=df.columns)
        if not shwdata:
            shwdata = df.columns
        st.dataframe(df[shwdata], use_container_width=True)

    # 주요 지표 계산
    total_questions = len(df)
    success_count = df[df['탈옥성공여부'] == 'success'].shape[0]
    fail_count = df[df['탈옥성공여부'] == 'fail'].shape[0]
    success_rate = (success_count / total_questions) * 100
    fail_rate = (fail_count / total_questions) * 100

    # 지표 출력
    total1, total2, total3, total4 = st.columns(4, gap='large')
    with total1:
        st.info('총 질문 수', icon="🔍")
        st.metric(label='Total', value=total_questions)
    with total2:
        st.info('성공 수', icon="🔍")
        st.metric(label='Success', value=success_count)
    with total3:
        st.info('실패 수', icon="🔍")
        st.metric(label='Fail', value=fail_count)
    with total4:
        st.info('성공률', icon="🔍")
        st.metric(label='Success Rate', value=f"{success_rate:.2f}%")

    st.markdown("""---""")

def Graphs():
    # 유형별 성공/실패 분포
    type_success_fail = df.groupby(['type', '탈옥성공여부']).size().reset_index(name='counts')
    fig_type_success_fail = px.bar(
        type_success_fail,
        x='type',
        y='counts',
        color='탈옥성공여부',
        title="유형별 성공/실패 분포",
        barmode='group',
        template="plotly_white"
    )
    fig_type_success_fail.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False)
    )

    # 성공/실패 비율 파이 차트
    success_fail_counts = df['탈옥성공여부'].value_counts().reset_index()
    success_fail_counts.columns = ['탈옥성공여부', 'counts']
    fig_success_fail_pie = px.pie(
        success_fail_counts,
        values='counts',
        names='탈옥성공여부',
        title='성공/실패 비율'
    )
    fig_success_fail_pie.update_layout(legend_title="탈옥성공여부", legend_y=0.9)
    fig_success_fail_pie.update_traces(textinfo='percent+label', textposition='inside')

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig_type_success_fail, use_container_width=True)
    right_column.plotly_chart(fig_success_fail_pie, use_container_width=True)

def ProgressBar():
    st.markdown(
        """<style>
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #99ff99 , #FFFF00);
        }
        </style>""",
        unsafe_allow_html=True,
    )
    target = 3000  # 목표 값 (예시)
    current = len(df)
    percent = round((current / target * 100))
    my_bar = st.progress(0)

    if percent > 100:
        st.subheader("Target 100% completed")
    else:
        st.write(f"현재 {percent}% 달성 (목표: {target:,d} 질문)")
        for percent_complete in range(percent):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)

def sideBar():
    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0,
        )
    if selected == "Home":
        try:
            HomePage()
            Graphs()
        except Exception as e:
            st.warning(f"An error occurred: {e}")

    if selected == "Progress":
        try:
            ProgressBar()
            Graphs()
        except Exception as e:
            st.warning(f"An error occurred: {e}")

# 사이드바 출력
sideBar()

# 푸터 설정
st.markdown(
    """
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"] {
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    [data-testid="stAppViewContainer"] {
        flex: 1;
    }
    .content {
        margin-bottom: 10rem; /* Add space between content and footer */
    }
    .footer {
        background-color: #f1f1f1;
        color: black;
        text-align: center;
        padding: 10px;
        margin-top: auto; /* Ensure footer is pushed to the bottom */
        width: 100%;
    }
    .footer a {
        color: #007BFF;
        text-decoration: none;
    }
    .footer-links {
        margin-top: 10px;
    }
    .footer-links a {
        margin: 0 10px;
        color: #007BFF;
        text-decoration: none;
    }
    .footer-author {
        margin-top: 10px;
    }
    .footer-version {
        background-color: #e0e0e0;
        padding: 5px;
        border-radius: 5px;
        display: inline-block;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="content"></div>', unsafe_allow_html=True)

# 푸터 콘텐츠
st.markdown(
    """
    <div class="footer">
        <div class="footer-links">
            <a href="https://www.kshieldjr.org/" target="_blank">KsheidJr.</a> |
            <a href="https://github.com/dashboard" target="_blank">Github</a>
        </div>
        <div class="footer-author">
            이메일: <a href="mailto:upsejong@gmail.com">upsejong@gmail.com</a><br>
            Copyright 2024 upsejong.<br>
            Powered by UpSejong.<br>
            <div class="footer-version">Version 1.0.1</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)











