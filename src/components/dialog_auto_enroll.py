
from src.database.config import supabase
import streamlit as st
import time




@st.dialog("Quick Enrollment")
def auto_enrole_dialog(join_code):
    student_id = st.session_state.student_data["student_id"]


    res = supabase.table("subjects").select("subject_id,subject_name").eq("subject_code",join_code).execute()

    if not res.data:
        st.error("Subject Code not found!!")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return
    subject = res.data[0]

    check = supabase.table("subject_students").select("*").eq("subject_id",subject['subject_id']).eq("student_id",student_id).execute()
    
    if check.data:
        st.info("You are allready Enrolled in this Subject")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
        return
    st.markdown(f"Would you Like to Enroll in **{subject['subject_name']}**?")
    c1,c2 = st.columns(2)
    with c1 :
        if st.button("Yes",type="primary",width="stretch"):
            supabase.table("subject_students").insert({"subject_id":subject['subject_id'],"student_id":student_id}).execute()
            st.success("Enrolled in Subject Successfully!")
            time.sleep(1)
            st.rerun()
    with c2:
        if st.button("No",type="secondary",width="stretch"):
            st.query_params.clear()
            st.rerun()