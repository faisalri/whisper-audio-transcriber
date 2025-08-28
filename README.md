# Whisper Audio Transcriber 🎙️

A simple and private web application for transcribing audio files to text, built with Streamlit and powered by OpenAI's open-source **Whisper** model.

## ✨ Key Features

- **Local Processing:** All transcription is done directly on your machine, ensuring your data remains private and secure. No files are uploaded to any external server.
- **Model Selection:** Choose from various Whisper model sizes (`tiny`, `base`, `small`, `medium`) to balance transcription speed and accuracy.
- **User-Friendly Interface:** The app features a clean and intuitive interface, allowing you to get a transcription with just a few clicks.
- **Cross-Platform:** The application runs on any system with Python, including Windows, macOS, and Linux.

## ⚙️ Installation

To get the app up and running, follow these simple steps.

### Prerequisites

You need **Python 3.8 or higher** installed on your system.

### Step 1: Clone the Repository

Clone this project from GitHub to your local machine using Git.

```bash
git clone [https://github.com/faisalri/whisper-audio-transcriber.git](https://github.com/faisalri/whisper-audio-transcriber.git)
cd whisper-audio-transcriber
```

# Step 2: Set Up the Environment

- Create the virtual environment
`python -m venv venv`

# Step 3: Install Dependencies
`pip install -r requirements.txt`

## ⚠️ Troubleshooting: Missing FFmpeg

The whisper library, particularly when processing audio files like .mp3, .m4a, or .ogg, relies on a command-line tool called FFmpeg to handle the audio decoding and conversion. If you encounter a FileNotFoundError, it means FFmpeg is not installed or not in your system's PATH.

You can install FFmpeg with a package manager like Chocolatey in PowerShell.

PowerShell

`choco install ffmpeg-full` 

Alternatively, you can manually download the builds from a trusted source and add them to your system's PATH.

Builds - CODEX FFMPEG @ gyan.dev

## 🚀 How to Run the App
Once you've completed the installation, you can launch the application from your terminal.

Bash

`streamlit run app.py`
Your web browser will automatically open and display the application, ready for you to transcribe your first audio file.

## 💻 Powered By
This application is built on top of the powerful and open-source Whisper model, developed by OpenAI.

You can find the original model repository on GitHub:
https://github.com/openai/whisper

## 🤝 Contributing
We welcome contributions from everyone! If you find a bug or have an idea for a new feature, feel free to open an issue or submit a pull request.

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for more details.