
import streamlit as st
from src.database.db import create_subject



@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of the subject you want to add")

    sub_name = st.text_input("Subject Name",placeholder="Subject Name")
    sub_id = st.text_input("Subject Code",placeholder="Subject Code")
    sub_section = st.text_input("Subject Section",placeholder="Subject Section")

    if st.button("Create Subject Now!!", type="primary", width="stretch"):
        if sub_id and sub_name and sub_section :
            try :
                create_subject(sub_id,sub_name,sub_section,teacher_id)
                st.toast("Subejct Created Successfully!", icon="✅")
                import time
                time.sleep(1)
                st.rerun()
            except Exception as e:
                st.error(e)
        else:
            st.warning("Please fill all the fields", icon="⚠️")

