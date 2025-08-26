import streamlit as st
import whisper
import os

st.set_page_config(layout="wide")

# ---
# NEW: Initialize session state to control transcription process
# This prevents the transcription from running automatically on each rerun.
if 'transcribe_started' not in st.session_state:
    st.session_state.transcribe_started = False
if 'audio_file_name' not in st.session_state:
    st.session_state.audio_file_name = None

# ---
# Function to format transcription based on a fixed duration.
# This function is unchanged from the previous version.
def format_by_duration(segments, duration=35):
    formatted_text = ""
    current_chunk_text = ""
    start_time = 0
    
    for segment in segments:
        if (segment['end'] - start_time) > duration and current_chunk_text != "":
            start_min = int(start_time // 60)
            start_sec = int(start_time % 60)
            end_min = int(segment['start'] // 60)
            end_sec = int(segment['start'] % 60)
            formatted_text += f"{start_min:02}:{start_sec:02} - {end_min:02}:{end_sec:02}\n"
            formatted_text += f"{current_chunk_text.strip()}\n\n"
            current_chunk_text = segment['text']
            start_time = segment['start']
        else:
            current_chunk_text += " " + segment['text']
            
    if current_chunk_text != "":
        start_min = int(start_time // 60)
        start_sec = int(start_time % 60)
        end_min = int(segments[-1]['end'] // 60)
        end_sec = int(segments[-1]['end'] % 60)
        formatted_text += f"{start_min:02}:{start_sec:02} - {end_min:02}:{end_sec:02}\n"
        formatted_text += f"{current_chunk_text.strip()}\n\n"
        
    return formatted_text

# ---
# Main Streamlit app components
st.title("Whisper Audio Transcriber App")

# ---
## Model Loading and Selection

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
## File Upload Section

# Store the file uploader widget in a variable to control its state.
uploaded_file = st.file_uploader(
    "Upload your audio file (.mp3, .wav, .m4a, etc.)",
    type=["mp3", "wav", "m4a", "ogg"]
)

# ---
# NEW: Functions for button actions
def start_transcription():
    st.session_state.transcribe_started = True

def reset_app():
    st.session_state.transcribe_started = False
    st.session_state.audio_file_name = None
    # We can't directly reset st.file_uploader, but resetting the session state
    # and rerunning the app will achieve the same effect for the user.
    st.experimental_rerun()

# ---
# NEW: Add a button to start the process and a reset button.
if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    col1, col2 = st.columns(2)
    with col1:
        st.button("Start Transcribe", on_click=start_transcription)
    with col2:
        st.button("Reset", on_click=reset_app)

    # ---
    # NEW: The transcription logic is now inside this conditional block.
    # It will only run if the 'transcribe_started' state is True.
    if st.session_state.transcribe_started:
        st.write("Starting transcription...")
        
        with st.status("Starting transcription...", expanded=True) as status:
            st.write("Preparing to transcribe audio...")
            
            os.makedirs("temp_audio", exist_ok=True)
            file_path = os.path.join("temp_audio", uploaded_file.name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.write("Transcribing audio to text...")
            
            result = model.transcribe(file_path, verbose=False)
            
            transcription_with_timestamps = format_by_duration(result["segments"], duration=35)
            
            status.update(label="Transcription complete!", state="complete", expanded=False)

        # --- Displaying Results ---
        st.subheader("Transcription Result:")

        st.text_area(
            label="Copy Transcription:",
            value=transcription_with_timestamps,
            height=300
        )

        st.download_button(
            label="Download as Text File",
            data=transcription_with_timestamps,
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}_transcription.txt",
            mime="text/plain"
        )
        
        os.remove(file_path)
        st.write("Temporary file has been removed.")
    
# --- The footnote remains unchanged ---
st.markdown("---")
st.markdown("### Developed by: [Faisal Riyadi](https://github.com/faisalri)")
st.markdown("#### Contact: faisalriyadi93@gmail.com")
st.markdown("_Consistency is key; keep learning, keep growing until you master it!_")