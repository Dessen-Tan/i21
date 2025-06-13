import streamlit as st
from audiorecorder import audiorecorder
import speech_recognition as sr
import io
import wave

st.title("Audio Recorder + Offline Transcription")

recorded_audio = audiorecorder("Click to record", "Stop recording")

if recorded_audio is not None and len(recorded_audio) > 0:
    audio_bytes = recorded_audio if isinstance(recorded_audio, (bytes, bytearray)) else bytes(recorded_audio)
    st.audio(audio_bytes, format="audio/wav")
    audio_buffer = io.BytesIO(audio_bytes)

    with wave.open(audio_buffer, 'rb') as wav_file:
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                st.text_area("Transcription", value=text, height=200)
            except sr.UnknownValueError:
                st.error("Speech Recognition could not understand audio")
            except sr.RequestError as e:
                st.error(f"Could not request results; {e}")
else:
    st.info("No audio recorded yet. Please record some audio.")

st.sidebar.info("Audio-to-Text page using SpeechRecognition")


