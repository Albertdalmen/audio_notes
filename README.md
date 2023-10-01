AudioNotes is a Python script designed to transcribe audio from either a YouTube video or a local audio file. It leverages the power of OpenAI's Whisper ASR system to convert spoken words into text. The transcriptions can be saved as .txt or .vtt (WebVTT) files.

## Prerequisites
Python: Ensure you have Python installed on your machine.
Dependencies: Install the required Python packages:

pip install openai-whisper pytube
FFmpeg: The script depends on FFmpeg. Ensure it's installed and available in your system's PATH.  

## Models
Whisper ASR models come in various sizes. Here are the available models:

English-only models:
tiny.en
base.en
small.en

Multilingual models:
tiny (1 GB, ~32x)
base (1 GB, ~16x)
small (2 GB, ~6x)
medium (5 GB, ~2x)
large (10 GB, 1x)
Note: The numbers like ~32x represent the speedup factor compared to the large model.

Supported Languages
English (en)
Spanish (es)
French (fr)
Catalan (ca)
...

# Usage
Run the script:
python <script_name>.py
Follow the on-screen prompts:

Choose the Whisper model.
Select the language.
Decide if you want to generate a .vtt subtitle file.
Choose the mode: Download a YouTube video or upload an audio file.
If you choose to download a YouTube video, provide the video URL. If you choose to upload an audio file, provide the absolute path to the file.

The script will transcribe the audio and save the transcription in the Transcripts directory. If you opted for a .vtt file, it will be saved alongside the .txt transcription.

# Class Overview
The main class in the script is AudioNotes. Here's a brief overview of its methods:

__init__: Initializes the class with the Whisper model, language, mode (YouTube or file), and audio path (if mode is file).
download_video: Downloads a YouTube video.
transcribe_audio: Transcribes the audio using the Whisper ASR system.
save_transcription: Saves the transcription as a .txt or .vtt file.
sanitize_filename: Sanitizes filenames by removing invalid characters.
Conclusion
AudioNotes is a handy tool for quickly transcribing audio from YouTube videos or local audio files. Whether you're a content creator, student, or professional, this tool can save you time and effort in converting spoken words into text.




