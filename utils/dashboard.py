import pandas as pd
import streamlit as st

# 데이터 로드 및 처리 함수
def load_results(filename):
    return pd.read_csv(filename)

def calculate_success_rate(results_df):
    grouped = results_df.groupby(['type']).agg(
        success_count=('탈옥성공여부', lambda x: (x == 'success').sum()),
        total_count=('탈옥성공여부', 'count')
    ).reset_index()
    grouped['success_rate'] = grouped['success_count'] / grouped['total_count']
    return grouped

class DashboardApp:
    def __init__(self):
        self.session_state = None

    def assign_session(self, session_state, app):
        self.session_state = session_state

    def run(self):
        st.markdown(
            """
            <style>
            .highlight-title {
                color: #000000;
                font-size: 1.5em;
                font-weight: bold;
            }
            .highlight-value {
                color: #000000;
                font-size: 2em;
                font-weight: bold;
            }
            .highlight-box {
                background-color: #EEEEEE;
                padding: 10px;
                border-radius: 5px;
                width: 100%;
            }
            .col-box {
                border: 1px solid #ddd;
                padding: 20px;
                margin: 10px;
                border-radius: 5px;
                background-color: #f1f1f1;
                box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            }
            .chart-title {
                background-color: #838383;
                color: white;
                padding: 10px;
                border-radius: 5px;
                text-align: left;
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown("<h1 style='font-size: 2.5em; color: #000000;'>🚀 Jailbreak Verification Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.5em;'>당신의 LLM 탈옥 가능성을 확인해보세요!</p>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

        results_df = load_results('/dataset/final_result_test.csv')
        total_cases = len(results_df)
        success_cases = (results_df['탈옥성공여부'] == 'success').sum()
        fail_cases = (results_df['탈옥성공여부'] == 'fail').sum()
        success_rate = success_cases / (success_cases + fail_cases) if (success_cases + fail_cases) > 0 else 0

        col1, col2, col3, col4 = st.columns(4)
        col1.markdown(f"<div class='highlight-box'><div class='highlight-title'>총 질문 수</div><div class='highlight-value'>{total_cases}</div></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='highlight-box'><div class='highlight-title'>성공한 탈옥 질문 수</div><div class='highlight-value'>{success_cases}</div></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='highlight-box'><div class='highlight-title'>실패한 탈옥 질문 수</div><div class='highlight-value'>{fail_cases}</div></div>", unsafe_allow_html=True)
        col4.markdown(f"<div class='highlight-box'><div class='highlight-title'>탈옥 성공률</div><div class='highlight-value'>{success_rate:.2%}</div></div>", unsafe_allow_html=True)
        st.markdown("<br><br>", unsafe_allow_html=True)

        grouped_df = calculate_success_rate(results_df)

        col1, col2 = st.columns([1, 1])

        with col1:
            container1 = col1.container(border=True)
            with container1:
                st.markdown("<div class='chart-title'>Type별 데이터 비율</div>", unsafe_allow_html=True)
                st.markdown("<br><br>", unsafe_allow_html=True)
                if not grouped_df.empty:
                    pie_chart = {
                        'mark': {'type': 'arc', 'innerRadius': 50},
                        'encoding': {
                            'theta': {'field': 'total_count', 'type': 'quantitative'},
                            'color': {
                                'field': 'type',
                                'type': 'nominal',
                                'scale': {
                                    'range': ['#FFB3B3', '#FFD9B3', '#FFFFB3', '#B3FFB3', '#B3D9FF', '#D9B3FF']
                                }
                            },
                            'tooltip': [{'field': 'type', 'type': 'nominal'}, {'field': 'total_count', 'type': 'quantitative'}]
                        },
                        'data': {'values': grouped_df.to_dict(orient='records')}
                    }
                    st.vega_lite_chart(pie_chart, use_container_width=True)

        with col2:
            container2 = col2.container(border=True)
            with container2:
                st.markdown("<div class='chart-title'>Type별 탈옥 성공률</div>", unsafe_allow_html=True)
                st.markdown("<br><br>", unsafe_allow_html=True)
                if not grouped_df.empty:
                    grouped_df['success_rate'] *= 100  # Convert to percentage
                    bar_chart = {
                        'mark': 'bar',
                        'encoding': {
                            'x': {'field': 'type', 'type': 'nominal', 'axis': {'title': 'Type', 'labelAngle': 0}},
                            'y': {'field': 'success_rate', 'type': 'quantitative', 'axis': {'title': 'Success Rate (%)'}, 'format': '.1f'},
                            'color': {
                                'field': 'type',
                                'type': 'nominal',
                                'scale': {
                                    'range': ['#FFB3B3', '#FFD9B3', '#FFFFB3', '#B3FFB3', '#B3D9FF', '#D9B3FF']
                                }
                            },
                            'tooltip': [{'field': 'type', 'type': 'nominal'}, {'field': 'success_rate', 'type': 'quantitative', 'format': '.1f'}]
                        },
                        'data': {'values': grouped_df.to_dict(orient='records')}
                    }
                    st.vega_lite_chart(bar_chart, use_container_width=True)

if __name__ == "__main__":
    app = DashboardApp()
    app.run()






