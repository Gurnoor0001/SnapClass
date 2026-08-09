from src.database.config import supabase 
import bcrypt


def hash_pass(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

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