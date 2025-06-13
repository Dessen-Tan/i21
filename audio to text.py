from audiorecorder import audiorecorder
import streamlit as st
import io

st.set_page_config(layout="centered")
st.title("Record Audio and Save")

try:
    recorded_audio = audiorecorder("Click to start recording", "Click to stop")

    if recorded_audio is not None and len(recorded_audio) > 0:
        audio_bytes = recorded_audio.tobytes()

        st.audio(audio_bytes, format="audio/wav")

        bio = io.BytesIO(audio_bytes)
        bio.name = "recording.wav"
        bio.seek(0)

        st.download_button(
            label="Save Recording",
            data=bio,
            file_name="recording.wav",
            mime="audio/wav"
        )
    elif recorded_audio is not None and len(recorded_audio) == 0:
        st.info("No audio recorded yet. Click the button above to record.")

except AttributeError as e:
    st.error(f"AttributeError: {e}")
except TypeError as e:
    st.error(f"TypeError: {e}")
except Exception as e:
    st.error(f"Unexpected error: {e}")

st.sidebar.info("Record your audio and save it as WAV.")
