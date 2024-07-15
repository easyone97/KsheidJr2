import streamlit as st

class OWASPApp:
    def __init__(self):
        pass

    def assign_session(self, session_state, parent_app):
        self.session_state = session_state
        self.parent_app = parent_app

    def run(self):
        col0, col1, col2 = st.columns([1, 2, 9])
        with col0:
            st.empty()  # 왼쪽 공백 추가
        with col1:
            st.title("참고자료")

        st.markdown("<br><br>", unsafe_allow_html=True)

        # CSS 스타일 설정
        st.markdown("""
            <style>
            .stDownloadButton > button {
                background-color: #25646F;
                color: white;
                border: none;
                padding: 8px 16px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px;
            }
            .stDownloadButton > button:hover {
                background-color: #00BFFF;
            }
            .reference-container {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 100%;
                padding: 20px;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            }
            .reference-text {
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                padding-left: 20px;
            }
            .reference-text h3 {
                font-size: 24px;
                margin: 0;
            }
            .reference-text p {
                font-size: 18px;
                margin: 0;
            }
            .reference-item {
                display: flex;
                align-items: center;
                justify-content: center;
                height: 100%;
            }
            </style>
        """, unsafe_allow_html=True)

        # 참고자료 항목들
        references = [
            {
                "title": "OWASP Top 10 for LLM",
                "description": "OWASP에서 발표한 LLM 애플리케이션에 영향을 미치는 가장 치명적인 취약점 상위 10가지",
                "image": "Images/owasp.jpeg",
                "file": "Downloadfile/OWASP-Top-10-for-LLMs-2023-v1_1.pdf"
            },
            {
                "title": "2024 LLM 한국형 보안 가이드라인",
                "description": "프롬프트 주입 공격(탈옥)에 중점을 둔 LLM 한국형 보안 안내서 <br> by K-Shield Jr 12기 Team.세종업고튀어",
                "image": "Images/가이드라인.jpeg",
                "file": "Downloadfile/2024-LLM-한국형-보안-가이드라인.pdf"
            },
            {
                "title": "한국어 탈옥 프롬프트 데이터셋 (2024-07-17 ver)",
                "description": "한국어 탈옥 프롬프트 공격의 실효성을 확인할 수 있는 데이터셋 (지속 업데이트 예정)",
                "image": "Images/checklist.png",
                "file": "Downloadfile/jailbreakPrompt.csv"
            }
        ]

        # 참고자료 항목 표시
        for index, ref in enumerate(references):
            col0, col123, col4 = st.columns([1, 10, 1])
            with col0:
                st.empty()  # 왼쪽 공백 추가
            with col123:
                with st.container(border=True):
                    col1, col2, col3 = st.columns([2, 6, 2])
                    with col1:
                        st.image(ref["image"], width=150)
                    with col2:
                        st.markdown(
                            f"""
                            <div class="reference-text">
                                <h3>{ref['title']}</h3>
                                <p>{ref['description']}</p>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    with col3:
                        with open(ref["file"], "rb") as file:
                            st.download_button(
                                label="PDF 다운로드" if ref["file"].endswith(".pdf") else "CSV 다운로드", 
                                data=file, 
                                file_name=ref["file"].split("/")[-1], 
                                mime="text/csv" if ref["file"].endswith(".csv") else "application/pdf",
                                key=f"download_button_{index}"
                            )
            with col4:
                st.empty()  # 오른쪽 공백 추가

if __name__ == "__main__":
    app = OWASPApp()
    app.run()










