
import streamlit as st 
from src.components.header import header_dashboard
from src.ui.base_layout import style_base_layout_dashboard,style_base_layout

from src.database.db import create_teacher, check_teacher_exists ,teacher_login, get_teacher_subjects
from src.components.dialog_create_subejct import create_subject_dialog 
from src.components.subject_card import subject_card
from src.components.share_subject_dialog import share_subject_dialog
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
    
    st.divider()

    if st.session_state.current_teacher_tab == "take_attendence":
        teacher_tab_take_attendence()

    if st.session_state.current_teacher_tab == "manage_subject":
        teacher_tab_manage_subject()

    if st.session_state.current_teacher_tab == "attendence_records":
        teacher_tab_attendence_records()
        


def teacher_tab_take_attendence():
    st.header("Take Attendence",text_alignment="center")
    
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
            def share_btn(s=sub):
                if st.button(f"Share Code: {s['subject_name']}",key=f"share_{s['subject_code']}", icon="🔗"):
                    share_subject_dialog(s["subject_name"], s["subject_code"])

            subject_card(
                name = sub["subject_name"],
                code = sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback = share_btn
            )

    else:
        st.info("No Subjects Added Yet!")
        

    
def teacher_tab_attendence_records():
    st.header("Attendence Records",text_alignment="center")


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
                time.sleep(2)
                st.rerun()
            else:
                st.error("Invalid credentials")
                import time 
                time.sleep(2)
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
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)
                import time 
                time.sleep(2)
                st.rerun()
    
    with b2:
        if st.button("Login", key="Login_Button", shortcut="control+enter", width="stretch"):
            st.session_state.teacher_login_type="login"
            st.rerun()
        
