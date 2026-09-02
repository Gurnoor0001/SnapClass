import streamlit as st

import segno
import io



@st.dialog("Create New Subject")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "http://localhost:8501"
    join_url = f"{app_domain}/?join-code={subject_code}"
    st.header("Scan to join📱")

    qr = segno.make(join_url)

    out = io.BytesIO()
    qr.save(out, kind = "png", scale = 8)
    
    col1, col2 = st.columns(2,vertical_alignment="center")

    with col1:
        st.markdown("### Copy Link")
        st.code(join_url,language="txt")
        st.code(subject_code,language="txt")
        st.info("Share this link and subject code with your students to join the subject", icon = "📢")

        
        
    with col2:
       st.markdown("### Scan QR Code")
       st.image(out.getvalue(), use_container_width=True,caption=subject_name)
