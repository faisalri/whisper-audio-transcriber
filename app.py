import streamlit as st
import whisper
import os

st.set_page_config(layout="wide")

# ---
# Initialize session state to control transcription process
if 'transcribe_started' not in st.session_state:
    st.session_state.transcribe_started = False
if 'audio_file_name' not in st.session_state:
    st.session_state.audio_file_name = None
if 'transcription_result' not in st.session_state:
    st.session_state.transcription_result = ""

# ---
# Function to format transcription based on a fixed duration.
def format_by_duration(segments, duration=20):
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

uploaded_file = st.file_uploader(
    "Upload your audio file (.mp3, .wav, .m4a, etc.)",
    type=["mp3", "wav", "m4a", "ogg"]
)

def start_transcription():
    st.session_state.transcribe_started = True

def reset_app():
    st.session_state.transcribe_started = False
    st.session_state.audio_file_name = None
    st.session_state.transcription_result = ""

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    col1, col2 = st.columns(2)
    with col1:
        st.button("Start Transcribe", on_click=start_transcription)
    with col2:
        st.button("Reset", on_click=reset_app)
    
    # ---
    if st.session_state.transcribe_started and st.session_state.transcription_result == "":
        with st.status("Starting transcription...", expanded=True) as status:
            st.write("1. Saving audio file...")
            os.makedirs("temp_audio", exist_ok=True)
            file_path = os.path.join("temp_audio", uploaded_file.name)
            
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            st.write("2. Transcribing audio to text...")
            result = model.transcribe(file_path, verbose=False)
            
            st.write("3. Formatting transcription with timestamps...")
            formatted_text = format_by_duration(result["segments"], duration=20)
            
            st.write("4. Storing result in session state...")
            st.session_state.transcription_result = formatted_text
            
            st.write("5. Cleaning up temporary files...")
            os.remove(file_path)
            
            status.update(label="Transcription complete!", state="complete", expanded=False)
    
    # --- Displaying Results ---
    if st.session_state.transcription_result != "":
        st.subheader("Transcription Result:")
        st.text_area(
            label="Copy Transcription:",
            value=st.session_state.transcription_result,
            height=300
        )

        st.download_button(
            label="Download as Text File",
            data=st.session_state.transcription_result,
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}_transcription.txt",
            mime="text/plain"
        )
        
# --- FOOTER SECTION: UPDATED LAYOUT ---
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Developed by: [Faisal Riyadi](https://github.com/faisalri)")
    st.markdown("#### Contact: faisalriyadi93@gmail.com")
    st.markdown("_Powered by OpenAI's open-source Whisper model._")

with col2:
    st.markdown("<p style='text-align: right;'>_Consistency is key; keep learning, keep growing until you master it!_</p>", unsafe_allow_html=True)