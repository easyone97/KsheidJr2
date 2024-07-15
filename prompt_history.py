import pandas as pd
import streamlit as st

# 독립적인 함수로 분리하여 캐시 처리
@st.cache_data
def load_results(filename):
  return pd.read_csv(filename)

class PromptHistoryApp:
  def __init__(self):
    pass

  def assign_session(self, session_state, parent_app):
    self.session_state = session_state
    self.parent_app = parent_app

  def run(self):
    # 로딩 공간을 유지하기 위한 placeholder 생성
    placeholder = st.empty()

    with placeholder.container():
      st.markdown("<style>body {background-color: white;}</style>", unsafe_allow_html=True)
      st.markdown("<h1 style='font-size: 2.5em; color: #000000;'>로딩 중...</h1>", unsafe_allow_html=True)

    # 로딩 화면 표시
    with st.spinner('로딩 중...'):
      if 'results_df' not in st.session_state:
        st.session_state.results_df = load_results('Downloadfile/final_result_test.csv')

    # 로딩 완료 후 placeholder 업데이트
    with placeholder.container():
      st.markdown(
        """
        <style>
        .container-box {
          border: 1px solid #ddd;
          padding: 20px;
          border-radius: 5px;
          margin-bottom: 20px;
          background-color: #776B5D;
          color: white;
          position: relative;
        }
        .title {
          font-size: 2.5em;
          font-weight: bold;
          color: black;
        }
        .subtitle {
          font-size: 1.5em;
          margin-top: 20px;
          margin-bottom: 10px;
          color: black;
        }
        .filter-label {
          font-size: 1.2em;
          font-weight: bold;
          color: white;
          margin-bottom: 10px;
          background-color: #838383;
          padding: 5px;
          border-radius: 5px;
        }
        .radio-label {
          display: block;
          font-size: 1.5em;
          margin-bottom: 10px;
          color: white;
        }
        .apply-button {
          display: flex;
          justify-content: flex-end;
          margin-top: 10px;
          margin-bottom: 10px;
        }
        .spacer {
          margin-bottom: 10px;
        }
        .container-spacing {
          margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
      )
      st.markdown("<h1 style='font-size: 2.5em; color: #000000;'>탈옥 프롬프트 내역</h1>", unsafe_allow_html=True)
      st.markdown("<br><br>", unsafe_allow_html=True)

      if st.session_state.results_df.empty:
        st.warning("No data available to display.")
        return

      # 초기 선택 상태 설정
      if 'selected_types' not in st.session_state:
        st.session_state.selected_types = ["전체"]
      if 'selected_success' not in st.session_state:
        st.session_state.selected_success = "전체"

      # 레이아웃 설정
      col1, col2 = st.columns([2, 8])

      with col1:
        with st.container(border=True):
          st.markdown("<div class='filter-label'>Type 선택</div>", unsafe_allow_html=True)
          type_options = ["전체"] + st.session_state.results_df['type'].unique().tolist()
          selected_types = st.multiselect("", type_options, default=st.session_state.selected_types)
          st.markdown("<div class='apply-button'>", unsafe_allow_html=True)
          if st.button("적용", key="apply_button"):
            st.session_state.selected_types = selected_types
          st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='container-spacing'></div>", unsafe_allow_html=True)

        with st.container(border=True):
          st.markdown("<div class='filter-label'>탈옥 성공 여부 선택</div>", unsafe_allow_html=True)
          success_options_display = ["전체", "Success", "Fail"]
          success_options_actual = ["전체", "success", "fail"]
          selected_success_display = st.radio("", success_options_display, index=success_options_actual.index(st.session_state.selected_success))
          selected_success_actual = success_options_actual[success_options_display.index(selected_success_display)]
          st.session_state.selected_success = selected_success_actual
          st.markdown('<style>.stRadio > div {display: flex; flex-direction: column;}</style>', unsafe_allow_html=True)

      # 데이터 표시
      filtered_df = filter_data(st.session_state.results_df, st.session_state.selected_types, st.session_state.
                                if filtered_df.empty:
        st.warning("No data available to display.")
        return

      with col2:
        st.dataframe(filtered_df.style.set_table_styles(
            [{
              'selector': 'th',
              'props': [
                ('background-color', '#4CAF50'),
                ('color', 'black'),
                ('font-family', 'Arial, sans-serif'),
                ('font-size', '16px')
              ]
            },
            {
              'selector': 'td, th, .row_heading, .index_name',
              'props': [
                ('border', '2px solid #4CAF50'),
                ('background-color', 'white'),
                ('color', 'black')
              ]
            }]
          ).set_properties(**{
            'background-color': 'white',
            'color': 'black',
            'border': '1.3px solid black'
          }), height=800, use_container_width=True)

if __name__ == "__main__":
  app = PromptHistoryApp()
  app.run()
















