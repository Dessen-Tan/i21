from audiorecorder import audiorecorder
import streamlit as st
import io
import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(audio_segment):
    try:
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        st.warning("Could not understand audio.")
        return None
    except sr.RequestError as e:
        st.error(f"Speech Recognition API error: {e}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return None

def process_uploaded_audio(audio_bytes, file_extension):
    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format=file_extension)
    except Exception as e:
        st.error(f"Could not process uploaded audio: {e}")
        return
    st.audio(audio_bytes)
    transcription = transcribe_audio(audio_segment)
    if transcription:
        st.subheader("Transcription")
        st.text_area("Transcribed text:", transcription, height=200)
        st.download_button(
            "Download Transcription as TXT",
            data=transcription,
            file_name="transcription.txt",
            mime="text/plain",
        )

st.set_page_config(layout="centered")
st.title("Record or Upload Audio to Transcribe & Save")

recorded_audio = audiorecorder("Click to record", "Stop recording")

if recorded_audio is not None and len(recorded_audio) > 0:
    if isinstance(recorded_audio, AudioSegment):
        audio_segment = recorded_audio
    else:
        st.error(f"Unsupported audio data format: {type(recorded_audio)}")
        audio_segment = None
    if audio_segment:
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)
        wav_bytes = wav_io.read()
        st.audio(wav_bytes, format="audio/wav")
        transcription = transcribe_audio(audio_segment)
        if transcription:
            st.subheader("Transcription")
            st.text_area("Transcribed text:", transcription, height=200)
            st.download_button(
                "Download Transcription as TXT",
                data=transcription,
                file_name="transcription.txt",
                mime="text/plain",
            )
        st.download_button(
            "Download Recorded Audio as WAV",
            data=wav_bytes,
            file_name="recorded_audio.wav",
            mime="audio/wav",
        )
else:
    st.info("Click the record button to start recording.")

st.subheader("Or upload an audio file to transcribe")
uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, M4A, etc.)")

if uploaded_file is not None:
    file_ext = uploaded_file.name.split('.')[-1].lower()
    audio_bytes = uploaded_file.read()
    process_uploaded_audio(audio_bytes, file_ext)

st.sidebar.info("Audio recorder, uploader, and transcription app without API keys.")

