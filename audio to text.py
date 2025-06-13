import streamlit as st
from audiorecorder import audiorecorder
import io
from pydub import AudioSegment
import speech_recognition as sr

st.title("Record Audio & Transcribe ")

transcription_placeholder = st.empty()
transcription_placeholder.text_area("Transcription will appear here...", value="", height=200, key="transcription_placeholder")

recorded = audiorecorder("Click to record", "Stop recording")

if recorded and len(recorded) > 0:
    audio_bytes = recorded.tobytes()
    st.audio(audio_bytes, format="audio/wav")

    audio_seg = AudioSegment(
        data=audio_bytes,
        sample_width=recorded.sample_width,
        frame_rate=recorded.sample_rate,
        channels=recorded.channels
    )
    wav_io = io.BytesIO()
    audio_seg.export(wav_io, format="wav")
    wav_io.seek(0)

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

