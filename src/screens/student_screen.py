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




def _check_cooldown():
    """Check if the user is in a failed-login cooldown period. Returns True if blocked."""
    failed_attempts = st.session_state.get("login_failed_attempts", 0)
    cooldown_until = st.session_state.get("login_cooldown_until", 0)
    
    if failed_attempts >= 3 and time.time() < cooldown_until:
        remaining = int(cooldown_until - time.time())
        st.error(f"🔒 Too many failed attempts. Please wait **{remaining}s** before trying again.")
        return True
    
    # Reset if cooldown has expired
    if failed_attempts >= 3 and time.time() >= cooldown_until:
        st.session_state.login_failed_attempts = 0
        st.session_state.login_cooldown_until = 0
    
    return False

def _record_failed_attempt():
    """Record a failed login attempt and trigger cooldown if threshold reached."""
    attempts = st.session_state.get("login_failed_attempts", 0) + 1
    st.session_state.login_failed_attempts = attempts
    
    if attempts >= 3:
        st.session_state.login_cooldown_until = time.time() + 30  # 30 second cooldown


def _verify_liveness(embed1, embed2):
    """
    Verify liveness by comparing two face embeddings:
    - They must be from the SAME person (distance < 0.45)
    - They must be DIFFERENT enough to confirm it's not a static photo (distance > 0.05)
    """
    distance = np.linalg.norm(np.array(embed1) - np.array(embed2))
    same_person = distance < 0.45
    not_static = distance > 0.05  # If distance is near-zero, it's likely the same static image
    return same_person and not_static


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
            # Clean up login state on exit
            for key in ["login_phase", "login_candidate", "login_embed1", "last_photo_id", 
                        "scan_result", "last_verify_photo_id", "login_failed_attempts", "login_cooldown_until"]:
                st.session_state.pop(key, None)
            st.rerun()
           
    
    # Initialize login phase
    if "login_phase" not in st.session_state:
        st.session_state.login_phase = "scan"  # "scan" or "verify"

    # Check cooldown before showing anything
    if _check_cooldown():
        return

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PHASE 1: Initial Face Scan
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    if st.session_state.login_phase == "scan":
        st.header("Login Using Face Recognition",text_alignment="center")
        st.caption("Step 1 of 2 — Initial face scan")
        st.space()

        photos = st.camera_input("Position Your Face in the center")

        if photos:
           # Only scan once per photo — cache results in session state
           photo_id = photos.file_id
           if st.session_state.get("last_photo_id") != photo_id:
               img = np.array(Image.open(photos))
               with st.spinner("AI is Scanning Your Face..."):
                   detected, all_ids, num_faces = predict_attendence(img)
                   # Also store the embedding for liveness check
                   embed = get_face_embed(img)
                   st.session_state.last_photo_id = photo_id
                   st.session_state.scan_result = {
                       "detected": detected,
                       "all_ids": all_ids,
                       "num_faces": num_faces,
                       "embedding": embed[0].tolist() if embed else None
                   }

           scan = st.session_state.get("scan_result", {})
           detected = scan.get("detected", {})
           num_faces = scan.get("num_faces", 0)

           if num_faces == 0:
                st.warning("No Face Detected")
                _record_failed_attempt()

           elif num_faces > 1:
                st.warning("Multiple Faces Detected — only one face allowed for login")
                _record_failed_attempt()

           else:
                if detected and scan.get("embedding"):
                   student_id = list(detected.keys())[0]
                   all_students = get_all_students()
                   student = next((s for s in all_students if s["student_id"]==student_id), None)

                   if student:
                    # Move to verification phase
                    st.session_state.login_phase = "verify"
                    st.session_state.login_candidate = student
                    st.session_state.login_embed1 = scan["embedding"]
                    st.toast(f"Face matched! Please verify it's you.", icon="🔐")
                    time.sleep(0.3)
                    st.rerun()
                   else:
                    st.info("Face Not Recognised ! you might be a new Student")
                    show_registration = True

                else:
                    st.info("Face Not Recognised ! you might be a new Student")
                    _record_failed_attempt()
                    show_registration = True 

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # PHASE 2: Liveness Verification (Second Photo)
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    elif st.session_state.login_phase == "verify":
        candidate = st.session_state.get("login_candidate", {})
        st.header("Verify Your Identity", text_alignment="center")
        st.caption("Step 2 of 2 — Liveness check")
        st.space()
        
        st.info(f"👤 Detected: **{candidate.get('student_name', 'Unknown')}**  \nPlease **turn your head slightly** or **change your expression** and take another photo to confirm it's really you.")
        
        verify_photo = st.camera_input("Take a verification photo", key="verify_camera")
        
        col_cancel, _ = st.columns([1, 3])
        with col_cancel:
            if st.button("← Start Over", key="restart_login"):
                st.session_state.login_phase = "scan"
                for key in ["login_candidate", "login_embed1", "last_verify_photo_id"]:
                    st.session_state.pop(key, None)
                st.rerun()
        
        if verify_photo:
            verify_photo_id = verify_photo.file_id
            if st.session_state.get("last_verify_photo_id") != verify_photo_id:
                st.session_state.last_verify_photo_id = verify_photo_id
                
                img2 = np.array(Image.open(verify_photo))
                with st.spinner("Verifying your identity..."):
                    embed2_list = get_face_embed(img2)
                    
                    if not embed2_list or len(embed2_list) != 1:
                        st.warning("Please ensure exactly one face is visible.")
                        _record_failed_attempt()
                    else:
                        embed1 = st.session_state.login_embed1
                        embed2 = embed2_list[0].tolist()
                        
                        if _verify_liveness(embed1, embed2):
                            # Liveness confirmed — log in
                            student = st.session_state.login_candidate
                            st.session_state.is_logged_in = True
                            st.session_state.user_type = "student"   
                            st.session_state.student_data = student   
                            # Clean up login state
                            for key in ["login_phase", "login_candidate", "login_embed1", 
                                        "last_photo_id", "last_verify_photo_id", "scan_result",
                                        "login_failed_attempts", "login_cooldown_until"]:
                                st.session_state.pop(key, None)
                            st.toast(f"Welcome {student['student_name']}",icon="👋")
                            time.sleep(0.5)
                            st.rerun()
                        else:
                            st.error("⚠️ Verification failed — the faces don't match, or a static image was detected. Please try again.")
                            _record_failed_attempt()
                            # Reset back to scan phase
                            st.session_state.login_phase = "scan"
                            for key in ["login_candidate", "login_embed1"]:
                                st.session_state.pop(key, None)
                            time.sleep(1.5)
                            st.rerun()

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

    