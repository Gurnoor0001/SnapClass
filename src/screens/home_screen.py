import streamlit as st 
from src.components.header import header_home
from src.ui.base_layout import style_base_layout_home,style_base_layout
def home_screen():

    header_home()

    style_base_layout_home()
    style_base_layout()

    col1, col2 = st.columns(2,gap="large")

    with col1:
        st.markdown('<h2 style="line-height: 1.2; margin-bottom: 15px;">Teacher <br/> Login</h2>', unsafe_allow_html=True)
        st.image("https://i.ibb.co/CsmQQV6X/mascot-prof.png",width = 144,)
        st.button("Teacher", on_click=lambda: st.session_state.update({"login_type": "teacher"}),width = 120)

    with col2:
        st.markdown('<h2 style="line-height: 1.2; margin-bottom: 15px;">Student <br/> Login</h2>', unsafe_allow_html=True)
        st.image("https://i.ibb.co/844D9Lrt/mascot-student.png",width = 130)
        st.button("Student", on_click=lambda: st.session_state.update({"login_type": "student"}),width = 120)