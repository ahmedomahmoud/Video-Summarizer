from pydub import AudioSegment
import os
from openai import OpenAI
from dotenv import load_dotenv
import subprocess

load_dotenv() 

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)


def transcribe_and_save_srt(audio_file_path: str, output_srt_path: str = None) -> str:
    """
    Transcribes an audio file, saves the result to an SRT file, and returns the path.

    This function assumes the directory for the output_srt_path already exists.
    It is memory-efficient as it returns the file path instead of the content.

    Args:
        audio_file_path: The path to the input audio file.
        output_srt_path (optional): The full path for the output .srt file.
                                    If not provided, it defaults to the same name
                                    as the audio file, but with an .srt extension,
                                    saved in the same directory.

    Returns:
        The full, absolute path to the saved .srt file.
    """
    print(f"Starting transcription for: {audio_file_path}")

    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Input audio file not found at: {audio_file_path}")

    # Determine the final output path
    if output_srt_path:
        final_srt_path = output_srt_path
    else:
        # Default behavior: save alongside the original audio file
        base_path, _ = os.path.splitext(audio_file_path)
        final_srt_path = base_path + ".srt"

    # Expand '~' to the user's home directory for convenience
    full_path = os.path.expanduser(final_srt_path)

    try:
        # Request transcription from the API
        with open(audio_file_path, "rb") as audio_file:
            srt_transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                response_format="srt" 
            )
        
        # Write the result to the specified file, assuming the directory exists
        with open(full_path, 'w', encoding='utf-8') as srt_file:
            srt_file.write(srt_transcription)
            
        print(f"Transcription successful. SRT file saved at: {full_path}")
        
        # Return the path where the file was saved
        return full_path

    except FileNotFoundError:
        # This will now trigger if the output directory doesn't exist
        print(f"Error: The directory for the output path '{full_path}' does not exist.")
        raise
    except Exception as e:
        print(f"An error occurred during transcription or saving: {e}")
        raise


def extract_audio(video_path, output_format="mp3"):
    audio = AudioSegment.from_file(video_path)
    audio_path = os.path.splitext(video_path)[0] + f".{output_format}"
    audio.export(audio_path, format=output_format)
    return audio_path

def check_video_restrictions(video_file):
    max_size = 20 * 1024 * 1024  # 20 MB
    max_duration = 12 * 60       # 12 minutes in seconds
    errors = []
    if os.path.getsize(video_file) > max_size:
        errors.append("Error: Video file exceeds 20 MB limit.")
    try:
        result = subprocess.run([
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of",
            "default=noprint_wrappers=1:nokey=1", video_file
        ], capture_output=True, text=True)
        duration = float(result.stdout.strip())
        if duration > max_duration:
            errors.append("Error: Video duration exceeds 12 minutes limit.")
    except Exception as e:
        errors.append(f"Error checking video duration: {e}")
    return errors