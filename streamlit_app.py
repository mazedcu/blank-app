import streamlit as st

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
import os
import shutil
from datetime import datetime
from pathlib import Path
from pydub import AudioSegment

# Additional dependencies:
# pip install torch torchaudio resemble-enhance
# ffmpeg is still required for pydub format conversion.

# Define folder paths
UPLOAD_FOLDER = Path("uploads")
CONVERTED_FOLDER = Path("converted")
DENOISED_FOLDER = Path("denoised")

# Ensure folders exist
UPLOAD_FOLDER.mkdir(exist_ok=True)
CONVERTED_FOLDER.mkdir(exist_ok=True)
DENOISED_FOLDER.mkdir(exist_ok=True)

def convert_to_wav(input_path: Path, output_path: Path) -> None:
    """
    Converts any supported audio file to WAV format using pydub.
    """
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")

def reduce_noise_with_resemble_enhance(input_path: Path, output_path: Path) -> None:
    """
    Applies noise reduction using the open-source Resemble Enhance model.
    Resemble Enhance is a deep learning-based speech denoiser and enhancer,
    providing high-quality results with options for dereverberation and intensity control.
    """
    from resemble_enhance.enhancer.inference import denoise

    # Load audio as waveform and sample rate
    import torchaudio
    wav, sr = torchaudio.load(input_path)

    # Denoise (adjust parameters as needed: solver iterations, dereverberation alpha, denoising strength)
    # Default values provide good results; increase nfe for better quality (slower), alpha for dereverb.
    denoised_wav, new_sr = denoise(wav, sr, device="cpu")  # Use "cuda" if GPU available

    # Save the enhanced audio
    torchaudio.save(output_path, denoised_wav.cpu(), new_sr)

def process_new_file(file_path: Path) -> None:
    """
    Processes a single uploaded file: converts to WAV, then applies AI-based noise reduction.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = file_path.stem
    
    # Step 1: Convert to WAV (preserves original sample rate)
    converted_path = CONVERTED_FOLDER / f"{base_name}_{timestamp}.wav"
    convert_to_wav(file_path, converted_path)
    print(f"Converted: {file_path.name} -> {converted_path.name}")
    
    # Step 2: Apply Resemble Enhance noise reduction
    denoised_path = DENOISED_FOLDER / f"{base_name}_{timestamp}_denoised.wav"
    reduce_noise_with_resemble_enhance(converted_path, denoised_path)
    print(f"Denoised (using Resemble Enhance AI model): {converted_path.name} -> {denoised_path.name}")

def monitor_folder() -> None:
    """
    Continuously monitors the upload folder for new files.
    """
    processed_files = set()
    
    print("Monitoring upload folder for new audio files...")
    
    while True:
        try:
            for file_path in UPLOAD_FOLDER.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in {".mp3", ".wav", ".ogg", ".flac", ".m4a", ".aac"}:
                    if file_path not in processed_files:
                        print(f"New file detected: {file_path.name}")
                        process_new_file(file_path)
                        
                        # Move original to processed subfolder
                        archive_folder = UPLOAD_FOLDER / "processed"
                        archive_folder.mkdir(exist_ok=True)
                        shutil.move(str(file_path), archive_folder / file_path.name)
                        
                        processed_files.add(file_path)
            
            import time
            time.sleep(5)
        
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user.")
            break
        except Exception as e:
            print(f"Error during monitoring: {e}")

if __name__ == "__main__":
    monitor_folder()