import streamlit as st
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

# External dependencies
try:
    from audiorecorder import audiorecorder
    AUDIO_RECORDER_AVAILABLE = True
except ModuleNotFoundError:
    AUDIO_RECORDER_AVAILABLE = False

# Load env variables (make sure you have .env with OPENAI_API_KEY)
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OpenAI API key not found. Please set OPENAI_API_KEY in your environment.")
    st.stop()

client = OpenAI(api_key=api_key)

st.title("Record Audio & Transcribe with Whisper")

# Placeholder for transcription text area before recording
transcription_placeholder = st.empty()
transcription_placeholder.text_area("Transcription will appear here...", value="", height=200, key="transcription_placeholder")

if AUDIO_RECORDER_AVAILABLE:
    recorded_audio = audiorecorder("Click to record", "Stop recording")
else:
    st.warning("Audio recording is disabled. Please ensure 'streamlit-audiorecorder' is installed and listed in requirements.txt.")
    recorded_audio = None

if recorded_audio and len(recorded_audio) > 0:
    # Convert recorded audio to bytes
    audio_bytes = recorded_audio.tobytes()

    # Display the audio player
    st.audio(audio_bytes, format="audio/wav")

    # Prepare BytesIO for OpenAI API
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "recorded_audio.wav"

    try:
        with st.spinner("Transcribing audio. Please wait..."):
            transcription_response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                prompt="Transcribe the audio with punctuation and capitalization."
            )
            transcription_text = transcription_response.text

        # Update the placeholder with the transcription result
        transcription_placeholder.text_area("Transcription:", value=transcription_text, height=200)

    except Exception as e:
        st.error(f"Error during transcription: {e}")
elif recorded_audio is not None and len(recorded_audio) == 0:
    st.info("No audio recorded yet. Please click 'Click to record' and then stop to capture audio.")
else:
    st.info("Click the button above to start recording.")

st.sidebar.info("This is the Audio-to-Text transcription page.")
