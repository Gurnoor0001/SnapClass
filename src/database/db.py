from src.database.config import supabase 
import bcrypt


def hash_pass(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=10)).decode()

def check_teacher_exists(username):
    # check unique username 
    response = supabase.table("teachers").select("teacher_user_name").eq("teacher_user_name",username).execute()

    return len(response.data) > 0 


def create_teacher(name, username, password, email):

    data = {
        "teacher_user_name": username, 
        "teacher_password": hash_pass(password), 
        "teacher_name": name,
        "teacher_email": email
    }
    response = supabase.table("teachers").insert(data).execute()
    return response
    

def teacher_login(username,password):
    response = supabase.table("teachers").select("*").eq("teacher_user_name",username).execute()
    if len(response.data) == 0:
        return False, "Teacher not found"
    
    stored_hash = response.data[0]["teacher_password"]
    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return True, response.data[0]
    else:
        return False, "Invalid password"


def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data



def create_student(new_name, face_embed, voice_embed=None):
    data = {"student_name":new_name,
            "face_embedding":face_embed,
            "voice_embedding":voice_embed
            }

    responce = supabase.table("students").insert(data).execute()
    return responce.data


def create_subject(subject_code, subject_name, section, teacher_id):
    data = {
        "subject_code":subject_code,
        "subject_name":subject_name,
        "section":section,
        "teacher_id":teacher_id
    }
    
    response = supabase.table("subjects").insert(data).execute()
    return response

def get_teacher_subjects(teacher_id):
    response = supabase.table("subjects").select("*, subject_students(count), attendance_logs(timestamp)").eq("teacher_id",teacher_id).execute()
    subjects =  response.data

    for sub in subjects:
        sub["total_students"] = sub.get("subject_students",[{}])[0].get("count") if sub.get("subject_students") else 0
        attendance_logs = sub.get("attendance_logs",[])
        unique_sessions = len(set(log["timestamp"]for log in attendance_logs))
        sub["total_classes"] = unique_sessions

        sub.pop("subject_students",None)
        sub.pop("attendance_logs",None)
      
        

    return subjects

def enroll_student_to_subject(student_id, subject_id):
    responce = supabase.table("subject_students").insert({"student_id":student_id,"subject_id":subject_id}).execute()
    return responce.data

def unenroll_student_to_subject(student_id, subject_id):
    responce = supabase.table("subject_students").delete().eq("student_id",student_id).eq("subject_id",subject_id).execute()

    return responce.data


def get_enrolled_subjects(student_id):
    response = supabase.table("subject_students").select("*,subjects(*)").eq("student_id",student_id).execute()
    return response.data


def get_attendance_logs(student_id):
    response = supabase.table("attendance_logs").select("*,subjects(*)").eq("student_id",student_id).execute()
    return response.data


def get_attendance_for_teacher(teacher_id):
    response = supabase.table("attendance_logs").select("*, subjects!inner(*)").eq("subjects.teacher_id",teacher_id).execute()
    return response.data

def delete_subject(subject_id):
    # Delete related attendance logs
    supabase.table("attendance_logs").delete().eq("subject_id", subject_id).execute()
    # Delete related enrollments
    supabase.table("subject_students").delete().eq("subject_id", subject_id).execute()
    # Delete the subject itself
    response = supabase.table("subjects").delete().eq("subject_id", subject_id).execute()
    return response.data
