

import streamlit as st
from audiorecorder import audiorecorder
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

st.title("Record Audio & Transcribe with Whisper")

# Placeholder text area before transcription
transcription_placeholder = st.empty()
transcription_placeholder.text_area("Transcription will appear here...", value="", height=200)

recorded_audio = audiorecorder("Click to record", "Stop recording")

if recorded_audio:
    audio_bytes = recorded_audio.tobytes()
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "recorded_audio.wav"

    with open("recorded_audio.wav", "wb") as f:
        f.write(audio_bytes)

    st.audio(audio_bytes, format="audio/wav")

    try:
        transcription_response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            prompt="Transcribe the audio with punctuation and capitalization."
        )
        transcription_text = transcription_response.text

        # Update placeholder with actual transcription
        transcription_placeholder.text_area(
            "Transcription:", 
            value=transcription_text, 
            height=200
        )
    except Exception as e:
        st.error(f"Error during transcription: {e}")
else:
    st.info("Click the button above to start recording.")

    
st.sidebar.info("This is the Speech-to-Text page.")
