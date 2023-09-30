""" Transcribes the audio file sent to it,
in case of video it's first converted to audio
using ffmpeg then the audio is then transcribed
"""
import openai
import os
import subprocess
video = "ayilara.mp4"
audio = "ayi.mp3"
ffmpeg_command = ['ffmpeg', '-i', video, '-vn', '-acodec', 'libmp3lame', audio,]
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
openai.api_key = "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"
#os.getenv("OPENAI_API_KEY")
ffmpeg_process.wait()
return_code = ffmpeg_process.poll()
if return_code is None:
    print("Conversion still in progress")
else:
    if return_code == 0:
        print("Conversion completed successfully")
        audio_file = open("ayi.mp3", "rb")
        transcript = openai.Audio.translate("whisper-1", audio_file)
        print(transcript)
    else:
        print("Conversion failed with return code:", return_code)