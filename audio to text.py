from audiorecorder import audiorecorder
import streamlit as st
import io
import numpy as np
import speech_recognition as sr
from pydub import AudioSegment

def transcribe_audio(audio_bytes):
    try:
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="wav")
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

st.set_page_config(layout="centered")
st.title("Record, Transcribe & Save Audio")

recorded_audio = audiorecorder("Click to record", "Stop recording")

if recorded_audio is not None and len(recorded_audio) > 0:
    try:
        if isinstance(recorded_audio, np.ndarray):
            audio_bytes = recorded_audio.tobytes()
        elif isinstance(recorded_audio, bytes):
            audio_bytes = recorded_audio
        elif isinstance(recorded_audio, list):
            audio_bytes = np.array(recorded_audio).tobytes()
        else:
            st.error(f"Unsupported audio data format: {type(recorded_audio)}")
            audio_bytes = None

        if audio_bytes:
            audio_segment = AudioSegment(
                audio_bytes,
                frame_rate=44100,
                sample_width=2,
                channels=1
            )
            wav_io = io.BytesIO()
            audio_segment.export(wav_io, format="wav")
            wav_io.seek(0)
            wav_bytes = wav_io.read()

            st.audio(wav_bytes, format="audio/wav")

            transcription = transcribe_audio(wav_bytes)

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
    except Exception as e:
        st.error(f"Error processing audio: {e}")
else:
    st.info("Click the record button to start recording.")

st.sidebar.info("Audio recorder and transcription app, no API keys required.")
