import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from audiorecorder import audiorecorder
from pydub.exceptions import CouldntDecodeError
from openai import OpenAI


load_dotenv()
key = os.getenv('OPENAI_API_KEY')
MODEL = 'gpt-4o'
client = OpenAI(api_key = key)




st.set_page_config(layout="centered")


try:
    with st.expander("Show `requirements.txt` content", expanded=False):
        st.code(open("requirements.txt").read())
except FileNotFoundError:
    st.error("CRITICAL ERROR: `requirements.txt` file not found in the repository's root directory.")



try:
    from audiorecorder import audiorecorder
    AUDIO_RECORDER_AVAILABLE = True
except ModuleNotFoundError:
    st.warning("The audio recorder component is not available. Please ensure 'streamlit-audiorecorder' is in requirements.txt and reboot the app.")
    AUDIO_RECORDER_AVAILABLE = False


def process_and_transcribe(audio_bytes, source_type, file_extension=None):
    st.info(f"Processing audio from {source_type}... Please wait.")
    st.audio(audio_bytes)

    
    try:
        format_to_use = file_extension if file_extension else "wav"
        try:
            audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format=format_to_use)
            
        except CouldntDecodeError:
            st.error(
                f"Error: Could not decode the audio file. "
                f"The format '{format_to_use}' may be unsupported or the file is corrupt."
            )
            return

        wav_audio_bytes_io = io.BytesIO()
        audio_segment.export(wav_audio_bytes_io, format="wav")
        wav_audio_bytes_io.seek(0)

        r = sr.Recognizer()
        with sr.AudioFile(wav_audio_bytes_io) as source:
            st.write("Reading audio for transcription...")
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
        st.warning("Speech Recognition could not understand the audio. The speech might be unclear or the file may contain silence.")

    
    except sr.RequestError as e:
        st.error(f"Could not request results from Google's Speech Recognition service; check your internet connection: {e}")

    
    except Exception as e:
        st.error(f"An unexpected error occurred during transcription: {e}")



st.markdown("---")

st.subheader("Option 1: Transcribe an Audio File")
uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, M4A, etc.)", key="audio_uploader")

st.markdown("<h3 style='text-align: center; color: grey;'>OR</h3>", unsafe_allow_html=True)

st.subheader("Option 2: Record Audio Directly")

recorded_audio = audiorecorder("Click to record", "Stop recording")

if recorded_audio:  
    audio_bytes = recorded_audio.tobytes()
    
    import io
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "recorded_audio.wav" 

    st.audio(audio_bytes)

    st.title('Audio Transcript')
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        prompt="Provide an accurate transcription of the audio using punctuation and capitalization."
    )
    st.write(transcription.text)
else:
    st.info("Click the button above to start recording.")

    
st.sidebar.info("This is the Speech-to-Text page.")
