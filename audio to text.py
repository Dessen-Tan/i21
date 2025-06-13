import streamlit as st
from audiorecorder import audiorecorder
import io
from pydub import AudioSegment
import speech_recognition as sr
import numpy as np

st.title("Record Audio & Transcribe (No OpenAI)")

transcription_placeholder = st.empty()
transcription_placeholder.text_area("Transcription will appear here...", value="", height=200, key="transcription_placeholder")

recorded = audiorecorder("Click to record", "Stop recording")

if isinstance(recorded, np.ndarray) and recorded.shape[0] > 0:
    # Convert NumPy array to bytes manually
    audio_bytes = recorded.astype(np.int16).tobytes()

    # Create a WAV-compatible audio segment
    audio_seg = AudioSegment(
        data=audio_bytes,
        sample_width=2,
        frame_rate=44100,
        channels=1
    )
    wav_io = io.BytesIO()
    audio_seg.export(wav_io, format="wav")
    wav_io.seek(0)

    st.audio(wav_io, format="audio/wav")

    r = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_data = r.record(source)

    try:
        text = r.recognize_google(audio_data)
        transcription_placeholder.text_area("Transcription:", value=text, height=200)
    except sr.UnknownValueError:
        st.warning("Could not understand audio.")
    except sr.RequestError:
        st.error("Speech Recognition API error.")
else:
    st.info("Click to record audio above.")

