# pyrefly: ignore [missing-import]
from streamlit.components.v2 import presentation
# pyrefly: ignore [missing-import]
import dlib
import numpy as np 
# pyrefly: ignore [missing-import]
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()


    sp=dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    face_recognizer = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, face_recognizer
    

def get_face_embed(img_np):

    detector, sp, face_recognizer = load_dlib_models()

    faces = detector(img_np, 1)

    embeddings = []

    for face in faces:
        shape = sp(img_np, face)
        face_descriptor = face_recognizer.compute_face_descriptor(img_np, shape, 1)
        embeddings.append(np.array(face_descriptor))
    
    return embeddings 

@st.cache_resource
def get_trained_model():

    X = []
    y = []

    students = get_all_students()

    if not students:
        return None
    
    for student in students:
        embeddings = student.get("face_embedding")
        if embeddings:
          
            X.append(np.array(embeddings))
            y.append(student.get("student_id"))
    
    if len(X)  == 0:
        return None


    clf = SVC(kernel="linear", probability=True, class_weight="balanced")

    try:
        clf.fit(X,y)
    except ValueError:
        pass
    return {"clf":clf, "X":X, "y":y}
def train_classifire():

    st.cache_resource.clear()
    model_data = get_trained_model()
    return bool(model_data)


def predict_attendence(class_img):
    encoddings = get_face_embed(class_img)

    detected_student = {}

    model_data = get_trained_model()

    if not model_data:
        return {}, [], len(encoddings)
    
    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]
    

    all_students = sorted(list(set(y_train)))

    # Security thresholds
    resemblance_threshold = 0.45  # Tightened from 0.6 — dlib distance < 0.4 is very confident, 0.4-0.5 is likely match
    svm_confidence_threshold = 0.70  # Require ≥70% SVM probability

    for encodding in encoddings:
        predicted_id = None
        svm_confident = False

        if len(all_students) >= 2:
            # Use SVM classifier with confidence check
            predicted_id = int(clf.predict([encodding])[0])
            probabilities = clf.predict_proba([encodding])[0]
            max_prob = float(max(probabilities))
            svm_confident = max_prob >= svm_confidence_threshold
        else:
            # Single student — still must pass distance check (no free bypass)
            predicted_id = int(all_students[0])
            svm_confident = True  # Skip SVM confidence for single-student (only distance matters)

        # Distance-based verification (always enforced)
        student_embedding = X_train[y_train.index(predicted_id)]
        best_match_score = np.linalg.norm(student_embedding - encodding)

        # DUAL-LAYER: Both SVM confidence AND distance must pass
        if svm_confident and best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True

    
    return detected_student, all_students, len(encoddings)