""" Transcribes the audio file sent to it,
in case of video it's first converted to audio
using ffmpeg then the audio is then transcribed
"""
import openai
import os
import subprocess
def run_transcription(url):
    video = url
    audio = "audio.mp3"
    print(f"Gotten the video file: {url}")
    ffmpeg_command = ['ffmpeg', '-i', video, '-vn', '-acodec', 'libmp3lame', audio,]
    print("Starting subprocess")
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    openai.api_key = "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"
#os.getenv("OPENAI_API_KEY")
    ffmpeg_process.wait()
    print("Waiting for subprocess")
    return_code = ffmpeg_process.poll()
    if return_code is None:
        print("Conversion still in progress")
    else:
        if return_code == 0:
            print("Conversion completed successfully")
            audio_file = open("audio.mp3", "rb")
            transcript = openai.Audio.translate("whisper-1", audio_file)
            return transcript['text']
        else:
            print("Conversion failed with return code:", return_code)
