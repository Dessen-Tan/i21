from audiorecorder import audiorecorder

import streamlit as st
import io
import speech_recognition as sr
from pydub import AudioSegment

def process_and_transcribe(audio_bytes, source_type, file_extension=None):
    st.info(f"Processing audio from {source_type}... Please wait.")
    st.audio(audio_bytes)

    try:
        format_to_use = file_extension if file_extension else "wav"
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format_to_use)
        
        wav_audio_bytes_io = io.BytesIO()
        audio_segment.export(wav_audio_bytes_io, format="wav")
        wav_audio_bytes_io.seek(0)

        r = sr.Recognizer()
        with sr.AudioFile(wav_audio_bytes_io) as source:
            audio_data = r.record(source)

        st.info("Transcribing audio... This may take a moment.")
        transcribed_text = r.recognize_google(audio_data)

        st.subheader("Transcribed Text:")
        st.text_area("Transcription Result", transcribed_text, height=200, key=f"transcribed_text_{source_type}")
        st.success("Audio transcribed successfully!")

        st.download_button(
            label="Download Transcription as TXT",
            data=transcribed_text,
            file_name="transcription.txt",
            mime="text/plain",
            key=f"download_{source_type}"
        )

    except sr.UnknownValueError:
        st.warning("Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        st.error(f"Could not request results from Google's API: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


st.set_page_config(layout="centered")


st.subheader("Upload an Audio File to Transcribe")
uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, M4A, etc.)", key="audio_uploader")



if uploaded_file is not None:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    process_and_transcribe(uploaded_file.read(), source_type="uploaded_file", file_extension=file_ext)

st.sidebar.info("This is the Speech-to-Text page.")


