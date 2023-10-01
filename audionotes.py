import os 
import re 
import datetime 

import whisper # pip install openai-whisper
from pytube import YouTube # pip install pytube

## script depends on ffpmeg 

"""

list of English-only models:    tiny.en   base.en   small.en
list of Multilingua model:      tiny      base      small       medium    large
                                1 GB      1 GB      2GB         5 GB      10 GB 
                                ~32x      ~16x      ~6x         ~2x       1x
"""
# rellevant languages: fr(french) en(english) es(spanish) ca(catalan)

class AudioNotes():
    
    def __init__(self, whisper_model = 'base', language='en', mode = 'file', audio_path =''): 
        self.whisper_model = whisper_model
        self.language = language
        self.mode = mode

        self.audio_name = audio_path.split('\\')[-1].split('.')[0]
        self.audio_path = audio_path 
        
                
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.yt_save_path = os.path.join(current_directory, "YoutubeDownloads")
        if not os.path.exists(self.yt_save_path):
            os.makedirs(self.yt_save_path)
            
        self.transcript_save_path = os.path.join(current_directory, "Transcripts")
        if not os.path.exists(self.transcript_save_path):
            os.makedirs(self.transcript_save_path)
        
    def download_video(self, url):
        try:
            yt = YouTube(url)
            video = yt.streams.filter(file_extension='mp4').get_highest_resolution()
            self.videotitle = self.sanitize_filename(video.title) 
            self.videofile = self.videotitle+".mp4"
            video_path = os.path.join(self.yt_save_path, self.videofile)
            if os.path.exists(video_path): 
                print(f"[INFO]: '{self.videotitle}' video already exists in the directory. Skipping download! \n") 
            else:
                video.download(output_path=self.yt_save_path, filename=self.videofile)
                print(f'[INFO]: Download of "{self.videofile}" completed! \n')
                
        except Exception as e:
            print(f"An error occurred: {e} \n")

    def transcribe_audio(self):
        try:
            model = whisper.load_model(self.whisper_model)
            option = whisper.DecodingOptions(language=self.language, fp16=False)
            if self.mode == 'yt':
                file = os.path.join(self.yt_save_path, self.videofile)
            elif self.mode =='file': 
                file = self.audio_path
                
            try:
                self.result = model.transcribe(file)
            except FileNotFoundError:
                print("[ERROR]: File not found. Please check the path and try again. \n")
            
            transcript = self.result['text']
            print("[TRANSCRIPT]: \n", transcript, "\n")

        except Exception as e: 
            print(f"[ERROR]: {e} \n")

    def save_transcription(self, save_vtt = False): 
        if self.mode == 'yt':
            directory = self.videotitle
            target_txt = self.videotitle+".txt" 
        else:
            directory = self.audio_name
            target_txt = self.audio_name+".txt"
  
        transcript_path = os.path.join(self.transcript_save_path, directory)
        if not os.path.exists(transcript_path):
            os.makedirs(transcript_path)
            
        with open(os.path.join(transcript_path, target_txt), 'w') as f: 
            f.write(self.result['text'])
    
        if save_vtt: 
            target_vtt = target_txt.split('.')[0]+".vtt"
            with open(os.path.join(transcript_path, target_vtt),'w') as f: 
                for idx, segment in enumerate(self.result['segments']):
                    f.write(str(idx +1) + '\n')
                    f.write(str(datetime.timedelta(seconds=segment['start'])) + ' --> ' + str(datetime.timedelta(seconds=segment['end'])) + '\n')
                    f.write(segment['text'].strip() + '\n')
                    f.write('\n')
                     
    def sanitize_filename(self, filename):
        sanitized_name = re.sub(r'[\\/*?:"<>|]', "", filename)
        sanitized_name = sanitized_name.replace(" ", "_")
        return sanitized_name


def main():
    # Select model: 
    model_mapping = {
        '1': 'tiny',
        '2': 'base',
        '3': 'small',
        '4': 'large'
        }
    model_choice = input("Choose the whisper model (select 1 2 3 or 4): \n * 1 tiny \n * 2 base \n * 3 small \n * 4 large \n\n - 'base' is the default option \n")
    model_choice = model_mapping.get(model_choice, 'base')  # Default to 'base' if an invalid choice is made
    
    # Select language: 
    language_choice = input("Choose the language (available: en (default), es, fr, ...): ")
    if not language_choice:
        language_choice = 'en'
        
    # generate subtitle file? 
    vtt_choice = input("would you like to generate a vtt file? [y/N]")
    vtt_choice = True if vtt_choice == "y" else False 
    
    # mode: from youtube or from file: 
    mode_choice = input("Do you want to (select 1 or 2): \n * 1 Download a YouTube video  \n * 2 Upload an audio file \n")
    if mode_choice == "1":
        url = input("Enter the YouTube video URL: ")
        
        audio_notes = AudioNotes(mode='yt')
        audio_notes.download_video(url)
        audio_notes.transcribe_audio()
        audio_notes.save_transcription(vtt_choice)
            
    elif mode_choice == "2":
        file_path = input("Enter the (absolute) path to the audio file: ")
        
        audio_notes = AudioNotes(mode='file', audio_path=file_path)
        audio_notes.transcribe_audio()
        audio_notes.save_transcription(vtt_choice)
    else:
        print("Invalid choice!")

if __name__ =="__main__":  
    main() 
