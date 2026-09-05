
from src.database.config import supabase
import streamlit as st
from PIL import Image
import time



def show_attendance_result(df, logs):
        st.header("Attendence Report")

        st.dataframe(df, hide_index=True, width="stretch")
        
        col1, col2 = st.columns(2, vertical_alignment="center", gap="large")

        with col1:
            try:
                if st.button("Approve & Save Attendence", type="primary",icon=":material/check_circle:",width="stretch"):
                    for log in logs:
                        supabase.table("attendance").insert(log).execute()
                    st.toast("Attendence Saved Successfully!", icon="✅")
                    st.session_state.attendance_imgs = []
                    st.session_state.voice_attendance_results = None
                    st.rerun(scope="fragment")
            except Exception as e:
                st.error(f"Error: {e}")
        
        with col2:
            if st.button("Cancel", type="secondary",icon=":material/close:",width="stretch"):
                st.session_state.voice_attendance_results = None 
                st.session_state.attendance_imgs = []
                st.rerun()
@st.dialog("Voice Attendence Report")
def attendance_result_dialog(df, logs):
   show_attendance_result(df, logs)
        
        