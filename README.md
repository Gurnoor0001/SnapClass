<p align="center">
  <img src="https://i.ibb.co/YTYGn5qV/logo.png" alt="LookHere Logo" width="120"/>
</p>

<h1 align="center">LookHere</h1>

<p align="center">
  <b>AI-Powered Smart Attendance System using Face Recognition & Voice Identification</b>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-Framework-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Supabase-Database-3ECF8E?logo=supabase&logoColor=white" alt="Supabase"/>
  <img src="https://img.shields.io/badge/dlib-Face%20Recognition-008080" alt="dlib"/>
  <img src="https://img.shields.io/badge/PyTorch-Voice%20ID-EE4C2C?logo=pytorch&logoColor=white" alt="PyTorch"/>
</p>

---

## 📖 About

**LookHere** is an AI-powered classroom attendance system that automates attendance tracking using **face recognition** and **voice identification**. Teachers can take attendance by simply uploading photos of the classroom or recording audio — the AI detects and identifies students automatically.

Built with **Streamlit** for the frontend, **Supabase** (PostgreSQL) for the database, **dlib** for face recognition, and **Resemblyzer** for voice identification.

---

## ✨ Features

### 👩‍🏫 Teacher Portal
- **Secure Login & Registration** — bcrypt-hashed password authentication
- **Subject Management** — Create, share, and delete subjects
- **Face-Based Attendance** — Upload classroom photos → AI detects & identifies students
- **Voice-Based Attendance** — Record classroom audio → AI identifies students by voice
- **QR Code Sharing** — Generate QR codes and shareable links for students to join subjects
- **Attendance Records** — View historical attendance data with stats

### 👨‍🎓 Student Portal
- **Face Recognition Login** — Students log in by showing their face to the camera
- **One-Click Registration** — New students register with a photo and optional voice sample
- **Subject Enrollment** — Enroll via subject code, link, or QR code scan
- **Auto-Enrollment** — Join subjects instantly via shared URL with `?join-code=` parameter
- **Attendance Dashboard** — View enrolled subjects with present/absent/total stats
- **Unenroll** — Leave subjects anytime

### 🤖 AI Pipelines
- **Face Pipeline** — Uses dlib's HOG face detector + 128D face embeddings + SVM classifier
- **Voice Pipeline** — Uses Resemblyzer (d-vector embeddings) for speaker identification with audio segmentation via librosa

---

## 🏗️ Project Structure

```
LookHere/
├── app.py                          # Main entry point
├── requirements.txt                # Python dependencies
├── .streamlit/
│   ├── config.toml                 # Streamlit server config
│   └── secrets.toml                # Supabase credentials (not committed)
│
└── src/
    ├── database/
    │   ├── config.py               # Supabase client initialization
    │   └── db.py                   # All database CRUD operations
    │
    ├── pipelines/
    │   ├── face_pipeline.py        # Face detection, embedding & SVM classifier
    │   └── voice_pipeline.py       # Voice embedding & speaker identification
    │
    ├── screens/
    │   ├── home_screen.py          # Landing page (Teacher/Student selection)
    │   ├── teacher_screen.py       # Teacher login, dashboard & all tabs
    │   └── student_screen.py       # Student face login, dashboard & enrollment
    │
    ├── components/
    │   ├── header.py               # App logo/header components
    │   ├── subject_card.py         # Reusable subject card UI component
    │   ├── dialog_create_subejct.py    # Create new subject dialog
    │   ├── dialog_add_photo.py         # Add classroom photos dialog
    │   ├── dialog_attendance_result.py # Face attendance results & save dialog
    │   ├── dialog_attendance_voice.py  # Voice attendance processing dialog
    │   ├── dialog_enroll.py            # Manual subject enrollment dialog
    │   ├── dialog_auto_enroll.py       # Auto-enrollment via QR/link dialog
    │   └── share_subject_dialog.py     # QR code & link sharing dialog
    │
    └── ui/
        └── base_layout.py         # Global CSS styles & theming
```

---

## 🗄️ Database Schema (Supabase)

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   teachers   │       │     subjects     │       │    students      │
├──────────────┤       ├──────────────────┤       ├──────────────────┤
│ teacher_id   │──┐    │ subject_id       │    ┌──│ student_id       │
│ teacher_name │  │    │ subject_name     │    │  │ student_name     │
│ teacher_user │  └───▶│ subject_code     │    │  │ face_embedding   │
│ teacher_pass │       │ section          │    │  │ voice_embedding  │
│ teacher_email│       │ teacher_id (FK)  │    │  └──────────────────┘
└──────────────┘       └────────┬─────────┘    │
                                │              │
                    ┌───────────┴──────────┐   │
                    │                      │   │
              ┌─────┴──────────┐   ┌───────┴───┴────────┐
              │subject_students│   │  attendance_logs    │
              ├────────────────┤   ├─────────────────────┤
              │ subject_id(FK) │   │ subject_id (FK)     │
              │ student_id(FK) │   │ student_id (FK)     │
              └────────────────┘   │ is_present (bool)   │
                                   │ timestamp           │
                                   └─────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Supabase account** — [supabase.com](https://supabase.com)
- **CMake** — Required for building dlib (`pip install cmake`)

### 1. Clone the Repository

```bash
git clone https://github.com/Gurnoor0001/LookHere.git
cd LookHere
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> **Note (Windows):** If `dlib` fails to install, use the pre-built wheel:
> ```bash
> pip install dlib-bin
> ```
> For `resemblyzer`, install without dependencies to avoid `webrtcvad` build errors:
> ```bash
> pip install webrtcvad-wheels
> pip install --no-deps resemblyzer
> ```

### 4. Set Up Supabase

1. Create a new Supabase project
2. Create the following tables in your Supabase SQL editor:

```sql
-- Teachers table
CREATE TABLE teachers (
    teacher_id SERIAL PRIMARY KEY,
    teacher_name TEXT NOT NULL,
    teacher_user_name TEXT UNIQUE NOT NULL,
    teacher_password TEXT NOT NULL,
    teacher_email TEXT
);

-- Students table
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    student_name TEXT NOT NULL,
    face_embedding JSONB,
    voice_embedding JSONB
);

-- Subjects table
CREATE TABLE subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name TEXT NOT NULL,
    subject_code TEXT UNIQUE NOT NULL,
    section TEXT,
    teacher_id INTEGER REFERENCES teachers(teacher_id)
);

-- Subject-Student enrollment (many-to-many)
CREATE TABLE subject_students (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects(subject_id),
    student_id INTEGER REFERENCES students(student_id),
    UNIQUE(subject_id, student_id)
);

-- Attendance logs
CREATE TABLE attendance_logs (
    id SERIAL PRIMARY KEY,
    subject_id INTEGER REFERENCES subjects(subject_id),
    student_id INTEGER REFERENCES students(student_id),
    is_present BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
```

### 5. Configure Secrets

Create `.streamlit/secrets.toml`:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-public-key"
```

### 6. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🔧 How It Works

### Face Recognition Pipeline

1. **Detection** — dlib's HOG-based face detector locates faces in the image
2. **Embedding** — Each face is converted to a 128-dimensional feature vector using dlib's `face_recognition_model_v1`
3. **Classification** — An SVM classifier (trained on enrolled students' embeddings) predicts the student identity
4. **Verification** — Euclidean distance between the predicted embedding and stored embedding is checked against a threshold (0.6) to prevent false positives

### Voice Identification Pipeline

1. **Audio Loading** — Classroom audio is loaded at 16kHz using librosa
2. **Segmentation** — Audio is split into segments using `librosa.effects.split` (silence removal)
3. **Embedding** — Each segment is converted to a d-vector using Resemblyzer's `VoiceEncoder`
4. **Matching** — Cosine similarity is computed between segment embeddings and enrolled students' voice embeddings
5. **Thresholding** — Students with similarity ≥ 0.7 are marked present

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit |
| **Database** | Supabase (PostgreSQL) |
| **Face Detection** | dlib (HOG detector) |
| **Face Recognition** | dlib (128D embeddings) + scikit-learn (SVM) |
| **Voice Identification** | Resemblyzer (d-vector) + librosa |
| **Authentication** | bcrypt |
| **QR Code Generation** | segno |
| **Deep Learning** | PyTorch (Resemblyzer backend) |

---

## 📸 App Flow

```
                    ┌─────────────┐
                    │  Home Page  │
                    └──────┬──────┘
                           │
               ┌───────────┴───────────┐
               ▼                       ▼
      ┌─────────────────┐    ┌──────────────────┐
      │  Teacher Login   │    │  Student Login    │
      │  (Username/Pass) │    │  (Face Camera)    │
      └────────┬─────────┘    └────────┬──────────┘
               ▼                       ▼
      ┌─────────────────┐    ┌──────────────────┐
      │ Teacher Dashboard│    │ Student Dashboard │
      ├─────────────────┤    ├──────────────────┤
      │• Take Attendance │    │• Enrolled Subjects│
      │  - Upload Photos │    │• Attendance Stats │
      │  - Voice Record  │    │• Enroll/Unenroll  │
      │• Manage Subjects │    └──────────────────┘
      │  - Create/Delete │
      │  - Share QR Code │
      │• Attendance Logs │
      └─────────────────┘
```

---

## 👥 Authors

- **Gurnoor Singh** — [GitHub](https://github.com/Gurnoor0001)

---

## 📄 License

This project is for educational purposes.

---

<p align="center">
  Made with ❤️ using Streamlit + AI
</p>
