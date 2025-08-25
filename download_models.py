import whisper

print("--- Starting to download all Whisper models ---")

# List of models to download
models_to_download = ["tiny", "base", "small", "medium", "large"]

for model_name in models_to_download:
    print(f"Downloading model: {model_name}...")
    try:
        whisper.load_model(model_name)
        print(f"Successfully downloaded model: {model_name}")
    except Exception as e:
        print(f"Failed to download {model_name}. Error: {e}")

print("--- All downloads complete! ---")