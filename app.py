import streamlit as st
import whisper
import os

st.set_page_config(layout="wide")

# Set the title for the Streamlit app.
st.title("Whisper Audio Transcriber App")

# ---
## Model Loading and Selection

# Add a selectbox for the user to choose the Whisper model size.
model_name = st.selectbox(
    "Choose a Whisper model:",
    ("tiny", "base", "small", "medium")
)

@st.cache_resource
def load_whisper_model(name):
    st.write(f"Loading {name} model. Please wait...")
    return whisper.load_model(name)

model = load_whisper_model(model_name)
st.success(f"Model {model_name} successfully loaded!")

# ---
## File Upload and Transcription

# Create a file uploader widget.
audio_file = st.file_uploader(
    "Upload your audio file (.mp3, .wav, .m4a, etc.)",
    type=["mp3", "wav", "m4a", "ogg"]
)

if audio_file is not None:
    st.audio(audio_file, format='audio/wav')
    
    with st.status("Starting transcription...", expanded=True) as status:
        st.write("Preparing to transcribe audio...")
        
        os.makedirs("temp_audio", exist_ok=True)
        file_path = os.path.join("temp_audio", audio_file.name)
        
        with open(file_path, "wb") as f:
            f.write(audio_file.getbuffer())

        st.write("Transcribing audio to text...")
        
        # --- NEW: Get a detailed transcription result with segments ---
        result = model.transcribe(file_path, verbose=False)
        
        # --- NEW: Format the transcription with timestamps ---
        transcription_with_timestamps = ""
        for segment in result["segments"]:
            start_time = segment["start"]
            end_time = segment["end"]
            text = segment["text"]
            
            # Format time to MM:SS format
            start_min = int(start_time // 60)
            start_sec = int(start_time % 60)
            end_min = int(end_time // 60)
            end_sec = int(end_time % 60)
            
            # Build the formatted string
            transcription_with_timestamps += f"{start_min:02}:{start_sec:02} - {end_min:02}:{end_sec:02}\n"
            transcription_with_timestamps += f"{text.strip()}\n\n"
        
        status.update(label="Transcription complete!", state="complete", expanded=False)

    # --- Displaying Results ---
    st.subheader("Transcription Result:")

    # --- NEW: Use st.text_area for easy copy-paste ---
    st.text_area(
        label="Copy Transcription:",
        value=transcription_with_timestamps,
        height=300
    )

    # --- NEW: Add a download button ---
    st.download_button(
        label="Download as Text File",
        data=transcription_with_timestamps,
        file_name=f"{os.path.splitext(audio_file.name)[0]}_transcription.txt",
        mime="text/plain"
    )

    # Clean up by removing the temporary file.
    os.remove(file_path)
    st.write("Temporary file has been removed.")