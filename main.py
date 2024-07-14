import streamlit as st
import pandas as pd
import plotly.express as px
import time

# 페이지 설정
st.set_page_config(page_title="Descriptive Analytics", page_icon="🌎", layout="wide")

# CSS 스타일 로드
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 엑셀 파일 로드
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# 함수 정의

def HomePage():
    # 데이터프레임 출력
    with st.expander("🧭 My database"):
        shwdata = st.multiselect('Filter:', df.columns, default=[])
        st.dataframe(df[shwdata], use_container_width=True)

    # 주요 지표 계산
    total_investment = float(df['Investment'].sum())
    investment_mode = float(df['Investment'].mode()[0])
    investment_mean = float(df['Investment'].mean())
    investment_median = float(df['Investment'].median())
    rating = float(df['Rating'].sum())

    # 지표 출력
    total1, total2, total3, total4, total5 = st.columns(5, gap='large')
    with total1:
        st.info('Total Investment', icon="🔍")
        st.metric(label='Sum TZS', value=f"{total_investment:,.0f}")
    with total2:
        st.info('Most frequently', icon="🔍")
        st.metric(label='Mode TZS', value=f"{investment_mode:,.0f}")
    with total3:
        st.info('Investment Average', icon="🔍")
        st.metric(label='Mean TZS', value=f"{investment_mean:,.0f}")
    with total4:
        st.info('Investment Median', icon="🔍")
        st.metric(label='Median TZS', value=f"{investment_median:,.0f}")
    with total5:
        st.info('Ratings', icon="🔍")
        st.metric(label='Rating', value=rating)

    st.markdown("""---""")

def Graphs():
    total_investments = int(df["Investment"].sum())
    average_rating = round(df["Rating"].mean(), 1)
    star_rating = ":star:" * int(round(average_rating, 0))
    average_investment = round(df["Investment"].mean(), 2)

    # 막대 그래프
    investment_by_businessType = df.groupby(by=["BusinessType"]).count()[["Investment"]].sort_values(by="Investment")
    fig_investment = px.bar(
        investment_by_businessType,
        x="Investment",
        y=investment_by_businessType.index,
        orientation="h",
        title="Investment by Business Type",
        color_discrete_sequence=["#0083B8"] * len(investment_by_businessType),
        template="plotly_white"
    )
    fig_investment.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
    )

    # 선 그래프
    investment_by_state = df.groupby(by=["State"]).count()[["Investment"]]
    fig_state = px.line(
        investment_by_state,
        x=investment_by_state.index,
        y="Investment",
        title="Investment by Region",
        color_discrete_sequence=["#0083B8"] * len(investment_by_state),
        template="plotly_white"
    )
    fig_state.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False))
    )

    left_column, right_column, center = st.columns(3)
    left_column.plotly_chart(fig_state, use_container_width=True)
    right_column.plotly_chart(fig_investment, use_container_width=True)

    # 파이 차트
    with center:
        fig = px.pie(df, values='Rating', names='State', title='Regions by Ratings')
        fig.update_layout(legend_title="Regions", legend_y=0.9)
        fig.update_traces(textinfo='percent+label', textposition='inside')
        st.plotly_chart(fig, use_container_width=True)

def ProgressBar():
    st.markdown(
        """<style>
        .stProgress > div > div > div > div {
            background-image: linear-gradient(to right, #99ff99 , #FFFF00);
        }
        </style>""",
        unsafe_allow_html=True,
    )
    target = 3000000000
    current = df['Investment'].sum()
    percent = round((current / target * 100))
    my_bar = st.progress(0)

    if percent > 100:
        st.subheader("Target 100% completed")
    else:
        st.write(f"현재 {percent}% 달성 (목표: {target:,d} TZS)")
        for percent_complete in range(percent):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1, text="Target percentage")

# 메뉴 탭 구현
selected_tab = st.sidebar.radio("메뉴 선택", ["Dashboard", "Progress", "Graphs"])

if selected_tab == "Dashboard":
    HomePage()
elif selected_tab == "Progress":
    ProgressBar()
elif selected_tab == "Graphs":
    Graphs()

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








