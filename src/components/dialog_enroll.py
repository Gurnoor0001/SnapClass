
from src.database.config import supabase
import streamlit as st
import time




@st.dialog("Enroll in subject")
def enroll_dialog():
    st.write("Enter the subject code provided by your Teacher")
    code = st.text_input("Subject Code",placeholder="Subject Code")

    if st.button("Enroll Now", type = "primary", icon=":material/check:"):
        if code:
            res = supabase.table("subjects").select("subject_id, subject_name, subject_code").eq("subject_code", code).execute() 
            if res.data:
               subject = res.data[0]
               student_id = st.session_state.student_data["student_id"]
               check = supabase.table("subject_students").select("*").eq("subject_id",subject['subject_id']).eq("student_id",student_id).execute()
               if check.data:
                   st.warning("Already Enrolled in this Subject")
               else:
                   supabase.table("subject_students").insert({"subject_id":subject['subject_id'],"student_id":student_id}).execute()
                   st.success("Enrolled in Subject Successfully!")
                   time.sleep(1)
                   st.rerun()
            else:
                st.error("Subject Not Found")
        else:
            st.warning("Please enter a subject code")
    
