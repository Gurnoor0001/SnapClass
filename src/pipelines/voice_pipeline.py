# pyrefly: ignore [missing-import]
from resemblyzer import VoiceEncoder, preprocess_wav 
import numpy as np 
import io 
# pyrefly: ignore [missing-import]
import librosa
import streamlit as st 
from src.database.db import get_all_students

@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    try :
        encoder = load_voice_encoder()

        audio,_ = librosa.load(io.BytesIO(audio_bytes),sr = 16000)

        wav = preprocess_wav(audio)

        embedding = encoder.embed_utterance(wav)

        return embedding.tolist()


    except Exception as e:
        st.error(f"error in voice encoding: {e}")
        return None
    

def identify_student_voice(new_embeddings, candidate_dict, threshold=0.6):
    if new_embeddings is None or not candidate_dict:
        return None, 0.0

    best_student_id = None

    best_score = float("-inf")

    for student_id, store_embed in candidate_dict.items():

        if store_embed:
            similarity =np.dot(new_embeddings, store_embed)
            if similarity > best_score:
                best_score = similarity
                best_student_id = student_id
    
    if best_score < threshold:
        return None, 0.0

    return best_student_id, best_score


def process_bulk_voice(audio_byte, candidate_dict, threshold = 0.6):
    try :
        encoder = load_voice_encoder()
        audio, sr = librosa.load(io.BytesIO(audio_byte), sr=16000)
        segments = librosa.effects.split(audio, top_db=25)
        identify_result = {}

        for start , end in segments:

            if((end-start) < sr*0.5):
                continue
            
            segment_audio = audio[start:end]
            wav = preprocess_wav(segment_audio)
            embedding = encoder.embed_utterance(wav)


            student_id, score = identify_student_voice(embedding, candidate_dict, threshold) 

            if student_id:
                if student_id not in identify_result or  score > identify_result[student_id]:
                    identify_result[student_id] = score
            
        
        return identify_result

    except Exception as e:
        st.error(f"error in voice processing: {e}")
        return {}

        

            
        


        
        


    



