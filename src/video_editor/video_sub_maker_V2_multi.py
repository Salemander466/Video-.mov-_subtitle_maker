#!/usr/bin/env python
# coding: utf-8

# In[15]:


get_ipython().system('pip install moviepy')
get_ipython().system('pip install nltk')
get_ipython().system('pip install SpeechRecognition')
get_ipython().system('pip install pysrt')
get_ipython().system('pip install pydub')


# In[16]:


get_ipython().system('pip install ffmpeg-python')


# In[16]:


get_ipython().system('pip install --upgrade google-cloud-speech')


# In[1]:





#Multi Video program

import os
import subprocess   
import nltk
from nltk.tokenize import word_tokenize
from moviepy.editor import VideoFileClip
import pysrt
from google.cloud import speech_v1p1beta1 as speech
import nltk
nltk.download('punkt')
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip
from pydub import AudioSegment
from pydub import effects

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\\Users\\teams\\Downloads\\groovy_secret.json"

def preprocess_audio(audio_path):
    # Load audio file
    audio = AudioSegment.from_file(audio_path)

    # Normalize volume
    audio = effects.normalize(audio)

    # Apply noise reduction (this might require `sox`)
    cmd = f'sox "{audio_path}" "{audio_path}" noisered'
    subprocess.run(cmd, shell=True)

    # Save processed audio
    audio.export(audio_path, format="wav")

def convert_mov_to_wav(video_path, audio_path):
    # Provide the full path to the stereo_audio.wav file
    mono_audio_path = "C:\\Users\\teams\\Untitled Folder\\mono_audio.wav"
    
    # Step 1: Extract mono audio from the video
    cmd1 = f'ffmpeg -y -i "{video_path}" -vn -acodec pcm_s16le -ac 1 "{mono_audio_path}"'
    result = subprocess.run(cmd1, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print('ffmpeg command failed')
        return None

    print(f'Mono audio extracted to {mono_audio_path}')

    # Preprocess audio
    preprocess_audio(mono_audio_path)

    # Check if the mono audio file was created correctly
    if not os.path.isfile(mono_audio_path):
        print(f'Error: {mono_audio_path} not found')
        return None

    return mono_audio_path

def speech_to_text(audio_path):
    client = speech.SpeechClient()
    with open(audio_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        enable_word_time_offsets=True,  # Enable timestamps
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90)  # Wait up to 90 seconds for the operation to complete

    # Create an empty list to hold all the words with their timestamps
    words = []
    for result in response.results:
        for word_info in result.alternatives[0].words:
            word = word_info.word
            start_time = word_info.start_time.total_seconds()
            end_time = word_info.end_time.total_seconds()
            words.append((word, start_time, end_time))

    return words

def convert_words_to_text(words):
    # concatenate words to form the text
    text = ' '.join(word for word, _, _ in words)
    return text

def create_srt(words, output_srt_path):
    subs = pysrt.SubRipFile()
    for i, word_info in enumerate(words):
        word, start_time, end_time = word_info

        # Convert start time and end time to pysrt.SubRipTime format
        start_time_srt = seconds_to_subrip_time(start_time)
        end_time_srt = seconds_to_subrip_time(end_time)

        sub = pysrt.SubRipItem(i, start=start_time_srt, end=end_time_srt, text=word.upper())
        subs.append(sub)

    subs.save(output_srt_path, encoding='utf-8')

def seconds_to_subrip_time(seconds):
    # Convert seconds to hours, minutes, seconds, milliseconds
    sec, ms = divmod(seconds, 1)
    ms = int(ms * 1000)
    min, sec = divmod(sec, 60)
    hour, min = divmod(min, 60)
    
    return pysrt.SubRipTime(hour, min, sec, ms)


# Define a list of colors for the subtitles
colors = ['red', 'green', 'blue', 'yellow']

# Define a list of fonts for the subtitles
fonts = ['Helvetica-Bold', 'Arial-Bold', 'Times-Roman', 'Courier']


#This will generate 4x4= 16 different videos. (e.g For each color it will generate 4 diffent video one for each font)
for i, color in enumerate(colors):
    for j, font in enumerate(fonts):
        # Use the color and font for the subtitles
        def add_subtitles_to_video(video_path, srt_path, output_path, color, font):
            generator = lambda txt: TextClip(txt, font=font, fontsize=56, color=color, align='center', stroke_color='black', kerning=6, stroke_width=1)
            sub = SubtitlesClip(srt_path, generator)
            sub = sub.set_position(('center', 250))  # Position subtitles at center of video
            clip = VideoFileClip(video_path)
            final = CompositeVideoClip([clip, sub])
            final.write_videofile(output_path, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)

        # Define the output video path
        output_video_path = f"output_{i}_{j}.mov"

        add_subtitles_to_video(video_path, output_srt_path, output_video_path, color, font)

video_path = r"C:\Users\teams\Untitled Folder\Thousands of disappearance’s.mov"
audio_path = "audio.wav"
output_srt_path = "output.srt"
output_video_path = "output.mov"

mono_audio_path = convert_mov_to_wav(video_path, audio_path) 
if mono_audio_path is not None:
    words = speech_to_text(mono_audio_path)
    transcript = convert_words_to_text(words)
    create_srt(words, output_srt_path)
    add_subtitles_to_video(video_path, output_srt_path, output_video_path)


# In[7]:





# In[9]:





# In[22]:





# In[43]:





# In[51]:





# In[ ]:




