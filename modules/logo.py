import streamlit as st
import base64
from pathlib import Path


def render_header(title="Suivi de consommation d'énergie", logo_path="data/logo_IPD.png"):
    logo_file = Path(logo_path)

    if logo_file.exists():
        logo_bytes = logo_file.read_bytes()
        logo_base64 = base64.b64encode(logo_bytes).decode()
        logo_html = f'<img src="data:image/png;base64,{logo_base64}">'
    else:
        logo_html = ""

    st.markdown(
        f"""
        <style>

        .app-header {{
            position: fixed;
            top: 3.5rem;
            left: 0;
            width: 100%;
            height: 95px;
            background-color: #0e1117;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            border-bottom: 1px solid #333;
        }}

        .app-header img {{
            height: 70px;
            margin-right: 18px;
        }}

        .app-title {{
            font-size: 42px;
            font-weight: 700;
            color: white;
        }}

        /* Push page content below fixed header */
        .block-container {{
            padding-top: 170px;
        }}

        </style>

        <div class="app-header">
            {logo_html}
            <div class="app-title">{title}</div>
        </div>
        """,
        unsafe_allow_html=True
    )