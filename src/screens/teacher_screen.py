
from itertools import groupby
from src.database.config import supabase
from src.pipelines.face_pipeline import predict_attendence
import streamlit as st 
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout_dashboard,style_base_layout
import numpy as np 

from src.database.db import create_teacher, check_teacher_exists ,teacher_login, get_teacher_subjects, delete_subject
from src.components.dialog_create_subejct import create_subject_dialog 
from src.components.subject_card import subject_card
from src.components.share_subject_dialog import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from datetime import datetime
import pandas as pd 
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_attendance_voice import voice_attendance_dialog
from src.database.db import get_attendance_for_teacher

def teacher_screen():
    style_base_layout_dashboard()
    style_base_layout()

    

    if "teacher_data" in st.session_state:
        teacher_dashboard()
        
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()

    elif st.session_state.teacher_login_type=="register":
        teacher_screen_register()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    c1,c2=st.columns(2,vertical_alignment="center",gap="large")

    with c1:
        header_dashboard()

    with c2:
        st.subheader("Welcome "+teacher_data["teacher_name"])
        if st.button("Logout",key = "Logout_Button", shortcut = "control+backspace"):
            st.session_state["is_logged_in"] = False
            del st.session_state.teacher_data
            st.rerun()
    


    st.space()
    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendence"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == "take_attendence" else "tertiary"
        if st.button("Take Attendence", type=type1,width = "stretch", icon=":material/photo_camera:"):
            st.session_state.current_teacher_tab = "take_attendence"
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == "manage_subject" else "tertiary"
        if st.button("Manage Subjects", type=type2,width = "stretch", icon=":material/menu_book:"):
            st.session_state.current_teacher_tab = "manage_subject"
            st.rerun()
        
    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == "attendence_records" else "tertiary"
        if st.button("Attendence Records", type=type3,width = "stretch", icon=":material/assignment:"):
            st.session_state.current_teacher_tab = "attendence_records"
            st.rerun()
    
    st.space()
    st.divider()
    st.space()

    if st.session_state.current_teacher_tab == "take_attendence":
        teacher_tab_take_attendence()

    if st.session_state.current_teacher_tab == "manage_subject":
        teacher_tab_manage_subject()

    if st.session_state.current_teacher_tab == "attendence_records":
        teacher_tab_attendence_records()
        


def teacher_tab_take_attendence():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    st.header("Take Attendence",text_alignment="center")

    if "attendance_imgs" not in st.session_state:
        st.session_state.attendance_imgs=[]

    subjects = get_teacher_subjects(teacher_id)
    
    if not subjects:
        st.warning("Please add subjects first")
        return 
    
    subjects_options = {f"{s['subject_name']}-{s['subject_code']}": s["subject_id"] for s in subjects }

    col1, col2 = st.columns([3,2],vertical_alignment="bottom")

    with col1:
        setected_sub_label = st.selectbox("Select Subject", options=list(subjects_options.keys()))
    with col2:
        if st.button("Take Attendence",key="take_attendance_btn",type="primary",icon=":material/photo_camera:",width="stretch"):
            add_photos_dialog()
    selected_subject_id = subjects_options[setected_sub_label]

    st.divider()    
            
    if st.session_state.attendance_imgs:
        st.header("Added Photos")
        gallery_cols = st.columns(4)

        for idx,img in enumerate(st.session_state.attendance_imgs):
            col = gallery_cols[idx % 4]
            with col:
                st.image(img, width="stretch", caption=f"Photo{idx+1}")
                

        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Clear All!",icon=":material/delete_sweep:",type="secondary",width="stretch"):
                st.session_state.attendance_imgs = []
                st.rerun()
        with c2:
            has_photos = bool(st.session_state.attendance_imgs)
            if st.button("Detect Faces",icon=":material/face:",type="primary",width="stretch",disabled=not has_photos):
                with st.spinner("Detecting Faces..."):
                    all_detected = {}

                    for idx, img in enumerate(st.session_state.attendance_imgs):
                        img_np = np.array(img.convert("RGB"))

                        detected, _, _ = predict_attendence(img_np)

                        if detected:
                            for sid in detected.keys():
                                student_id = int(sid)
                                all_detected.setdefault(student_id, []).append(f"Photo{idx+1}")

                    enrolled_res = supabase.table("subject_students").select("*, students(*)").eq("subject_id",selected_subject_id).execute()
                    enrolled_students = enrolled_res.data
                    if not enrolled_students:
                        st.warning("No Student enrolled in this course")
                    else:

                        results, attendance_to_logs = [], []

                        current_timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') 


                        for node in enrolled_students:
                            student = node["students"]
                            source = all_detected.get(int(student["student_id"]),[])
                            is_present = len(source)>0
                            results.append({
                                "Name" : student["student_name"],
                                "ID" : student["student_id"],
                                "Attendence" : "✅ Present" if is_present else "❌ Absent",
                                "Source":", ".join(source) if is_present else "--"
                            } )


                            attendance_to_logs.append({
                                "student_id" : student["student_id"],
                                "subject_id" : selected_subject_id,
                                "is_present" : is_present,
                                "timestamp" : current_timestamp
                            })
                        attendance_result_dialog(pd.DataFrame(results), attendance_to_logs)
                                
                
        with c3:
            if st.button("Voice Attendance",icon=":material/volume_up:",type="primary",width="stretch"):
                voice_attendance_dialog(selected_subject_id)
    
def teacher_tab_manage_subject():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    col1, col2 = st.columns(2)
    with col1:
        st.header("Manage Subjects",text_alignment="center")
    with col2:
        if st.button("Add Subject",type="primary",icon=":material/add:"):   
            create_subject_dialog(teacher_id)
    # list all Subjects

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("🫂","Students", sub["total_students"]),
                ("🕰️","classes", sub["total_classes"]),
            ]
            def footer_btns(s=sub):
                fc1, fc2 = st.columns(2)
                with fc1:
                    if st.button(f"Share Code: {s['subject_name']}",key=f"share_{s['subject_code']}", icon="🔗"):
                        share_subject_dialog(s["subject_name"], s["subject_code"])
                with fc2:
                    if st.button(f"Delete: {s['subject_name']}",key=f"delete_{s['subject_id']}", icon=":material/delete:", type="secondary"):
                        delete_subject(s["subject_id"])
                        st.toast(f"Subject '{s['subject_name']}' deleted!", icon="🗑️")
                        import time
                        time.sleep(0.5)
                        st.rerun()

            subject_card(
                name = sub["subject_name"],
                code = sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback = footer_btns
            )

    else:
        st.info("No Subjects Added Yet!")
        

    
def teacher_tab_attendence_records():
    st.header("Attendence Records",text_alignment="center")
    teacher_id = st.session_state.teacher_data["teacher_id"]

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        st.info("No Records Found")

    else:
        data = []

        for r in records:
            ts = r.get("timestamp")

            data.append(
                {
                    "ts_group":ts.split(".")[0]if ts else "N/A",
                    "Time":datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p")if ts else "N/A",
                    "Subject":r["subjects"]["subject_name"],
                    "Subject Code":r["subjects"]["subject_code"],
                    "is_present":bool(r.get("is_present", False))
                }
            )

        df_records = pd.DataFrame(data)

        summary = (
            df_records.groupby(["ts_group", "Time", "Subject", "Subject Code","is_present"])
            .agg(
                Present_Count =  ("is_present", "sum"),
                Total = ("is_present", "count")
            ).reset_index().sort_values("Time",ascending=False)
        )
        summary["Attendance Stats"] = (
            "✅"+ (summary["Present_Count"]).astype(str) + "/" + (summary["Total"]).astype(str)
            )


        display_df = (summary.sort_values(by="ts_group",ascending=False)
                        [["Time","Subject","Subject Code","Attendance Stats"]]        
                )

        st.dataframe(display_df,width="stretch", hide_index=True)

        

        



def register_teacher(teacher_name,teacher_user_name,teacher_user_email,teacher_user_pass,teacher_user_pass_confirm):
    if not teacher_user_name or not teacher_name or not teacher_user_email or not teacher_user_pass or not teacher_user_pass_confirm:
        return False, "All fields are required"
    
    if check_teacher_exists(teacher_user_name):
        return False, "Teacher already exists"

    if teacher_user_pass != teacher_user_pass_confirm:
        return False, "Passwords do not match"

    try:    
        create_teacher(teacher_name,teacher_user_name,teacher_user_pass,teacher_user_email)
        return True, "Teacher registered successfully"
    except Exception as e:
        return False, str(e)

def login_teacher(teacher_user_name,teacher_user_pass):
    if not teacher_user_name or not teacher_user_pass:
        return False, "All fields are required"    

    success, result = teacher_login(teacher_user_name,teacher_user_pass)
    if success:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data  = result
        st.session_state.is_logged_in = True
        return True
    
    else:
        return False

def teacher_screen_login():

    c1,c2=st.columns(2,vertical_alignment="center",gap="large")

    with c1:
        header_dashboard()

    with c2:
        if st.button("Back To Home",key = "Home_Button", shortcut = "control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    
    
    st.header("Login",text_alignment="center")
    st.markdown("")
    st.markdown("")
    st.markdown("")
    teacher_user_name = st.text_input("Enter your username",placeholder="Username") 
    teacher_user_pass = st.text_input("Enter your password",placeholder="Password",type="password") 
    
    st.divider()
    
    b1,b2 = st.columns(2,vertical_alignment="center")

    with b1:
        if st.button("Login", key="Login_Button", shortcut="enter", width="stretch"):
            if login_teacher(teacher_user_name,teacher_user_pass):
                st.toast("Welcome "+teacher_user_name, icon="✅")
                import time 
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Invalid credentials")
                import time 
                time.sleep(0.5)
                st.rerun()
                
    
    with b2:
        if st.button("Register", key="Register_Button", shortcut="control+enter", width="stretch"):
            st.session_state.teacher_login_type="register"

def teacher_screen_register():

    c1,c2=st.columns(2,vertical_alignment="center",gap="large")

    with c1:
        header_dashboard()


    with c2:
        if st.button("Back To Home",key = "Home Button", shortcut = "control+backspace"):
            st.session_state["login_type"] = None
            st.rerun()
    
    
    
    st.header("Register Your Teacher Profile", text_alignment="center")


    st.markdown("")
    st.markdown("")
    st.markdown("")
    teacher_name = st.text_input("Enter your name",placeholder="Name")
    teacher_user_name = st.text_input("Enter your username",placeholder="Username") 
    teacher_user_email = st.text_input("Enter your email",placeholder="Email")
    teacher_user_pass = st.text_input("Enter your password",placeholder="Password",type="password") 
    teacher_user_pass_confirm = st.text_input("Confirm your password",placeholder="Confirm Password",type="password") 
    
    st.divider()
    
    b1,b2 = st.columns(2,vertical_alignment="center")

    with b1:
        if st.button("Register", key="Register_Button", shortcut="enter", width="stretch"):
            success, message  = register_teacher(teacher_name,teacher_user_name,teacher_user_email,teacher_user_pass,teacher_user_pass_confirm)
            if success :
                st.success(message)
                import time 
                time.sleep(0.5)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)
                import time 
                time.sleep(0.5)
                st.rerun()
    
    with b2:
        if st.button("Login", key="Login_Button", shortcut="control+enter", width="stretch"):
            st.session_state.teacher_login_type="login"
            st.rerun()
        
