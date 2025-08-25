import streamlit as st
import whisper
import os

# Set the title for the Streamlit app.
st.title("Whisper Audio Transcriber App")

# ---
## Model Loading and Selection

# Add a selectbox for the user to choose the Whisper model size.
# Smaller models are faster but less accurate, while larger models are more accurate but require more resources.
model_name = st.selectbox(
    "Choose a Whisper model:",
    ("tiny", "base", "small", "medium")
)

# Use st.cache_resource to cache the model. This prevents the model from being reloaded
# every time the user interacts with the app, significantly speeding up the process.
@st.cache_resource
def load_whisper_model(name):
    """
    Loads the specified Whisper model from the local cache.
    If the model is not found, it will be downloaded automatically.
    """
    st.write(f"Loading {name} model. Please wait...")
    return whisper.load_model(name)

# Load the selected model.
model = load_whisper_model(model_name)
st.success(f"Model {model_name} successfully loaded!")

# ---
## File Upload and Transcription

# Create a file uploader widget.
# This widget handles the file input from the user.
audio_file = st.file_uploader(
    "Upload your audio file (.mp3, .wav, .m4a, etc.)",
    type=["mp3", "wav", "m4a", "ogg"]
)

# Check if a file has been uploaded before proceeding.
if audio_file is not None:
    st.audio(audio_file, format='audio/wav')
    st.write("Starting transcription...")
    
    # Create a temporary directory to store the uploaded audio file.
    # The whisper model requires a file path, so we can't directly use the uploaded file