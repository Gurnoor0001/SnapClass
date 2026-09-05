
from src.database.config import supabase
import streamlit as st
import time
from src.pipelines.voice_pipeline import process_bulk_voice
from datetime import datetime
import pandas as pd     
from src.components.dialog_attendance_result import show_attendance_result 



@st.dialog("Voice Attendence")
def voice_attendance_dialog(selected_subject_id):

   st.write("Recorde audio of student saying I am present")


   audio = None

   audio_data = st.audio_input("Record ClassRoom Audio")

   if st.button("Analyze Audio",type="secondary",icon=":material/analytics:",width="stretch"):
    with st.spinner("AI is Processing Audio..."):
        
        enrolled_res = supabase.table("subject_students").select("*, students(*)").eq("subject_id",selected_subject_id).execute()
        enrolled_students = enrolled_res.data

        
        if not enrolled_students:
            st.warning("No Student enrolled in this course")
            return
        else:

            candidates_dict = {
                s["students"]["student_id"]: s["students"]["voice_embedding"] 
                for s in enrolled_students if s['students'].get('voice_embedding')
            }


            if not candidates_dict:
                st.error("No Student have uploaded Voice")
                return 

            audio_bytes = audio_data.read()

            detected_scores = process_bulk_voice(audio_bytes,candidates_dict)
    
        
            results, attendance_to_logs = [], []

            current_timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') 


            for node in enrolled_students:
                student = node["students"]
                score = detected_scores.get(int(student["student_id"]), 0.0)
                
                is_present = score >= 0.7
                results.append({
                    "Name" : student["student_name"],
                    "ID" : student["student_id"],
                    "Attendence" : "✅ Present" if is_present else "❌ Absent",
                    "Confidence" : f"{score:.2f}" if is_present else "--"
                } )


                attendance_to_logs.append({
                    "student_id" : student["student_id"],
                    "subject_id" : selected_subject_id,
                    "is_present" : is_present,
                    "timestamp" : current_timestamp
                })
         
            st.session_state.voice_attendance_results = (
                pd.DataFrame(results),
                attendance_to_logs
            )
            

            if st.session_state.get("voice_attendance_results"):
                st.divider()
                df_res, logs = st.session_state.voice_attendance_results 

                show_attendance_result(df_res, logs)


   