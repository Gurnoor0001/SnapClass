from pipelines.face_pipeline import predict_attendence
from streamlit import spinner
import streamlit as st 
from PIL import Image 
import numpy as np 

from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout_dashboard, style_base_layout
# pyrefly: ignore [missing-import]
from src.pipelines.face_pipeline import predict_attendence


def student_screen():
    style_base_layout_dashboard()
    style_base_layout()


    c1,c2=st.columns(2,vertical_alignment="center",gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button("Back To Home",key = "Home_Button", shortcut = "control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    
    
    st.header("Login Using Face Recognistion",text_alignment="center")
    st.space()
    st.space()
    st.space()

    photos = st.camera_input("Position Your Face in the center")

    if photos:
       img =  np.array(Image.open(photos))

       with st.spinner("AI is Scanning Your Face..."):
        detected, all_ids, num_faces = predict_attendence(img)

        if num_faces == 0:
            st.warning("No Face Detected")

        elif num_faces > 1:
            st.warning("Multiple Face Detected")

        else:
            st.success("face Detected")
            
            
    