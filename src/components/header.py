import streamlit as st
import base64
import os

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def header_home():
    logo_path = "assets/logo.jpg"
    if os.path.exists(logo_path):
        logo_b64 = get_base64_image(logo_path)
        logo_url = f"data:image/jpeg;base64,{logo_b64}"
    else:
        logo_url = ""

    st.markdown(f"""
<div style = 'display: flex;flex-direction: column; align-items: center; justify-content: center;margin-bottom: 30px;margin-top: 30px;'>
    <img src ='{logo_url}'  style="height: 100px;">
    <h1 style = 'text-align: center;color:#E8E6F0;'>Look Here</h1>
<div/>
""",unsafe_allow_html=True)


def header_dashboard():
    logo_path = "assets/logo.jpg"
    if os.path.exists(logo_path):
        logo_b64 = get_base64_image(logo_path)
        logo_url = f"data:image/jpeg;base64,{logo_b64}"
    else:
        logo_url = ""

    st.markdown(f"""
<div style = 'display: flex; align-items: center; justify-content: center;gap: 10px;'>
    <img src ='{logo_url}'  style="height: 70px;">
    <h2 class="header-title" style = 'text-align: center;'>Look Here</h2>
<div/>
""",unsafe_allow_html=True)