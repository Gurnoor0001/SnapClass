from PIL.Image import enum
from src.database.db import get_all_students,create_student,get_enrolled_subjects,get_attendance_logs,unenroll_student_to_subject
import streamlit as st 
from PIL import Image 
import numpy as np 
import time

from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout_dashboard, style_base_layout
# pyrefly: ignore [missing-import]
from src.pipelines.face_pipeline import predict_attendence,get_face_embed,train_classifire
# pyrefly: ignore [missing-import]
from src.components.dialog_enroll import enroll_dialog
# pyrefly: ignore [missing-import]
from src.pipelines.voice_pipeline import get_voice_embedding 
# pyrefly: ignore [missing-import]
from src.components.subject_card import subject_card


def student_dashboard():
    student_data = st.session_state.student_data
    student_id = student_data["student_id"]
    c1,c2=st.columns(2,vertical_alignment="center",gap="large")

    with c1:
        header_dashboard()

    with c2:
        st.subheader("Welcome "+student_data["student_name"])
        if st.button("Logout",key = "Logout_Button", shortcut = "control+backspace"):
            st.session_state["is_logged_in"] = False
            del st.session_state.student_data
            st.rerun()
    
    st.space()

    col1, col2 = st.columns(2,vertical_alignment="center",gap="large")

    with col1:
        st.header("Your Enrolled Subjects",text_alignment="center")

    with col2:
        if st.button("Enroll in Subject",type="primary", width="stretch", icon=":material/add:"):
            enroll_dialog()

    
    st.divider()

    with st.spinner("Loading Enrolled Subjects..."):
        subjects = get_enrolled_subjects(student_id)
        attendance_logs = get_attendance_logs(student_id)
    
    stats_map = {}

    for log in attendance_logs:
        sub_id = log["subject_id"]

        if sub_id not in stats_map:
            stats_map[sub_id] = {"present":0, "total":0}

        stats_map[sub_id]["total"] += 1 

        if log.get("is_present"):
            stats_map[sub_id]["present"] += 1 

    cols = st.columns(2)
    for i , sub_node in enumerate(subjects):
        sub = sub_node["subjects"]
        sub_id = sub["subject_id"]
        stats = stats_map.get(sub_id, {"present": 0, "total": 0})
        def unenroll_button(sid=sub_id):
            if st.button("Unenroll",type="secondary", key=f"unenroll_{sid}",icon=":material/close:"):
                unenroll_student_to_subject(student_id,sid)
                st.toast("Unenrolled from Subject",icon="👋")
                st.rerun()

        with cols[i % 2]:
            subject_card(
                name = sub["subject_name"],
                code = sub["subject_code"],
                section = sub["section"],
                stats = [
                    ("📚", "Total Classes", stats["total"]),
                    ("✅", "Present", stats["present"]),
                    ("❌", "Absent", stats["total"] - stats["present"]),
                ],
                footer_callback = unenroll_button 
            )




def student_screen():
    show_registration = False
    style_base_layout_dashboard()
    style_base_layout()

    if "student_data" in st.session_state:
        student_dashboard()
        return
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
       # Only scan once per photo — cache results in session state
       photo_id = photos.file_id
       if st.session_state.get("last_photo_id") != photo_id:
           img = np.array(Image.open(photos))
           with st.spinner("AI is Scanning Your Face..."):
               detected, all_ids, num_faces = predict_attendence(img)
               st.session_state.last_photo_id = photo_id
               st.session_state.scan_result = {
                   "detected": detected,
                   "all_ids": all_ids,
                   "num_faces": num_faces
               }

       scan = st.session_state.get("scan_result", {})
       detected = scan.get("detected", {})
       num_faces = scan.get("num_faces", 0)

       if num_faces == 0:
            st.warning("No Face Detected")

       elif num_faces > 1:
            st.warning("Multiple Face Detected")

       else:
            if detected:
               student_id = list(detected.keys())[0]
               all_students = get_all_students()

               student = next((s for s in all_students if s["student_id"]==student_id), None)

               if student :
                st.session_state.is_logged_in =  True
                st.session_state.user_type = "student"   
                st.session_state.student_data = student   
                st.toast(f"Welcome {student['student_name']}",icon="👋")
                time.sleep(0.5)
                st.rerun()
               else:
                st.info("Face Not Recognised ! you might be a new Student")
                show_registration = True

            else:
                st.info("Face Not Recognised ! you might be a new Student")
                show_registration = True 

    if show_registration:
        with st.container(border=True):
            st.header("Register New Profile")

            new_name = st.text_input("Enter your Name", placeholder="Name")

            st.subheader("Optional : Voice Enrollment")
            st.info("Enroll for Voice Attendence Only !")


            audio_data = None 

            try:

                audio_data = st.audio_input("Record a Short phrase Like : I am Present, My name is .....", key="voice_enroll")               

            except Exception as e:
                st.error("Error Recording Audio : ", e)

            if st.button("Create Account", type = "primary"):
                if new_name:
                    with st.spinner("Creating Profile..."):
                        img = np.array(Image.open(photos))
                        encodding = get_face_embed(img)
                        if encodding: 
                            face_embed = encodding[0].tolist()
                            
                            voice_embed = None 
                            if audio_data:
                                audio_bytes = audio_data.getvalue()
                                voice_embed = get_voice_embedding(audio_bytes)

                            response_data = create_student (
                                new_name,face_embed,voice_embed
                            )

                            if response_data:
                                train_classifire()
                                st.session_state.is_logged_in =  True
                                st.session_state.user_type = "student"   
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Welcome {new_name}",icon="👋")
                                time.sleep(0.5)
                                st.rerun()
                                            
                            else:
                                st.error("Failed to Create Profile")
                else:   
                    st.warning("Name not Found !")    
    