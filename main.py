import streamlit as st
import pandas as pd
from hydralit import HydraApp

import dashboard
import prompt_history
import owasp
import llm_security


# Initialize HydraApp with the theme
app = HydraApp(title='🚀 Jailbreak Verification Dashboard', use_navbar=True, navbar_animation=True, navbar_theme=theme)

# Add main apps
app.add_app("Dashboard", app=dashboard.DashboardApp(), icon="🏠")
app.add_app("탈옥 프롬프트 내역", app=prompt_history.PromptHistoryApp(), icon="📚")
app.add_app("참고자료", app=owasp.OWASPApp(), icon="📘")

# Define the structure for complex navigation
complex_nav = {
    "Dashboard": ["Dashboard"],
    "탈옥 프롬프트 내역": ["탈옥 프롬프트 내역"],
    "참고자료": ["참고자료"]
}

if __name__ == '__main__':
    app.run(complex_nav=complex_nav)

  # Footer with "Powered by", "Contact Us", and version
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
            background-color: ##25646F;
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

    # Footer content
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











