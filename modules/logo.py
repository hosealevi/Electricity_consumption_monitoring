import streamlit as st
from PIL import Image
import os

def display_logo():
    logo_path = os.path.join("data", "logo_IPD.png")
    logo = Image.open(logo_path)

    col1, col2 = st.columns([1,6])

    with col1:
        st.image(logo, width=120)

    with col2:
        st.title("Energy Monitoring Dashboard")