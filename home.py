import streamlit as st
st.set_page_config(
    page_title="Multimodal Translator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Welcome to the Multimodal Translator! 🤖")
st.markdown("---")
st.header("What can this app do?")
st.markdown(
    """
    This application is a one-stop-shop for your translation needs. 
    It leverages powerful AI models to seamlessly convert between text and audio formats.
    
    Select a tool from the sidebar to get started!
    """
)

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.subheader("💬 Text to Audio Converter")
    st.info("Bring your text to life!")

with col2:
    st.subheader("🎤 Audio to Text Transcriber")
    st.info("Transcribe any speech!")
st.sidebar.success("Select a page above.")
st.sidebar.markdown("---")
st.sidebar.caption("This is made by Group I21.")
