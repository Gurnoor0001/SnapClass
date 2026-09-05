
from src.database.config import supabase
import streamlit as st
from PIL import Image
import time

def _next_photo_key():
    """Return a unique key suffix so camera/upload widgets reset after each addition."""
    if "photo_key_counter" not in st.session_state:
        st.session_state.photo_key_counter = 0
    st.session_state.photo_key_counter += 1
    return st.session_state.photo_key_counter




@st.dialog("Add Photos")
def add_photos_dialog():
    
    st.write("Add Classroom Photos to Scan for Attendance ")

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    t1,t2 = st.columns(2)
    with t1:
        type1 = "primary" if st.session_state.photo_tab == "camera" else "secondary"
        if st.button("Camera", type=type1, width="stretch", icon=":material/photo_camera:"):
            st.session_state.photo_tab = "camera"
            st.rerun(scope="fragment")
    with t2:
        type2 = "primary" if st.session_state.photo_tab == "upload" else "secondary"
        if st.button("Upload", type=type2, width="stretch", icon=":material/upload:"):
            st.session_state.photo_tab = "upload"
            st.rerun(scope="fragment")
    

    if "photo_key_counter" not in st.session_state:
        st.session_state.photo_key_counter = 0

    if st.session_state.photo_tab == "camera":
        photo = st.camera_input("Take Photo", key=f"photo_cam_{st.session_state.photo_key_counter}")

        if photo:
            st.session_state.attendance_imgs.append(Image.open(photo))
            st.toast("Photo Added Successfully!", icon="✅")
            _next_photo_key()
            st.rerun(scope="fragment")

    if st.session_state.photo_tab == "upload":
        photo = st.file_uploader("Upload Photo", type=["jpg","png","jpeg"], key=f"photo_up_{st.session_state.photo_key_counter}", accept_multiple_files=True)
        if photo:
            for img in photo:
                st.session_state.attendance_imgs.append(Image.open(img))
            st.toast("Photos Added Successfully!", icon="✅")
            _next_photo_key()
            st.rerun(scope="fragment")
    
    st.divider()
    if st.button("Done", type="primary", width="stretch"):
        st.rerun()