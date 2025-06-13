import streamlit as st
import io
from gtts import gTTS
import os

st.set_page_config(layout="centered") 

st.title("Text-to-Speech Converter")
st.markdown("Type in the text you want to convert to speech...")

text_input = st.text_area("Enter text here:", height=150, key="tts_text_area")

if st.button("Convert to Speech", key="convert_button"):
    if text_input:
        with st.spinner("Processing... Generating speech. Please wait."):
            try:
                tts = gTTS(text=text_input, lang='en', slow=False)


                audio_bytes_io = io.BytesIO()
                tts.write_to_fp(audio_bytes_io)
                audio_bytes_io.seek(0) 

                st.success("Text converted to speech successfully!")


                st.audio(audio_bytes_io.getvalue(), format='audio/mp3', start_time=0)

                download_fp = io.BytesIO(audio_bytes_io.getvalue())
                st.download_button(
                    label="Download Speech as MP3",
                    data=download_fp,
                    file_name="speech.mp3",
                    mime="audio/mp3",
                    key="download_button"
                )

            except Exception as e:
                st.error(f"An error occurred during speech generation: {e}")
    else:
        st.warning("Please enter some text to convert.")

st.sidebar.info("This is the Text-to-Speech page.")
