import moviepy.editor as mp 
from moviepy.config import change_settings
import speech_recognition as sr 
import configparser
import sys
import os

audio_duration = 0
change_settings({"IMAGEMAGICK_BINARY": "lib/ImageMagick-7.1.1-43-portable-Q16-HDRI-x64/magick.exe"})


# Loads the TOML config and converts it to SectionProxy
def load_config(conf_section):
    config = configparser.ConfigParser()
    try:   
        config.read("editor.conf")
    except KeyError:
        print("Config file is not using or key is not found.")
        return None
    if conf_section in config:
        return config[conf_section]
    else:
        print(f"{conf_section} section not found in config.")
        return None

def get_recognizer():
    recognizer_settings = load_config("RecognizerSettings")
    if recognizer_settings is not None:
        recognizer = recognizer_settings.get("recognizer", None)
        if recognizer:
            if recognizer == "whisper":
                print("Using whisper as voice recognizer")
                return recognizer
            elif recognizer == "google":
                print("Using google as voice recognizer")
                return "google"
            else: 
                print("Unknown recognizer! Just whisper supported. Using default recognizer: Google")
                return "google"
        else:
            print("'recognizer' key not found in the config section. Using default recognizer: Google")
            return "google"

    else:
        print("Failed to load configuration. Using default recognizer: Google")
        return "google"

def get_lang():
    recognizer_settings = load_config("RecognizerSettings")
    if recognizer_settings is not None:
        language = recognizer_settings.get("language", None)
        if language:
            if language == "en":
                print("Using en-GB as language")
                return "en-GB"
            elif language == "tr":
                print("Using tr-TR as language")
                return "tr-TR"
        else:
            print("'language' key not found in the config section. Using default language: tr")
            return "tr-TR"

    else:
        print("Failed to load configuration. Using default language: tr")
        return "tr-TR"

def edit(input_file, output_file):
    recognizer = get_recognizer()
    lang = get_lang()
    video = mp.VideoFileClip(input_file)

    # Create the text file from speech
    speech_text = get_text(input_file, recognizer, lang)
    print(f"Speech text generated! Word count: {len(speech_text.split())}")
    print("---------------------------")
    print(f"Speech text: {speech_text}")
    print("---------------------------")
    modify = input("Do you want to modify text? y/n: ")
    if modify == "y":
        speech_text = input("Enter the new entire text: ")

    # Parse the text to lines with 6 words, each line include max 6 words
    words = parse_text_to_words(speech_text)
    text_clips = []
    start_time = 0
    print(f"Audio duration is {audio_duration} seconds.")
    duration_for_each_word = audio_duration / len(words)
    # For each line, create TextClips
    for word in words:
        if word != "":
            text_duration = duration_for_each_word
            txt_clip = mp.TextClip(word, fontsize=150, color='yellow', font='Arial', stroke_color='black', stroke_width=1, method='label')
            txt_clip = txt_clip.set_start(start_time)
            # ### clip is at 40% of the width, 70% of the height:
            # >>> clip.set_position((0.4,0.7), relative=True)
            txt_clip = txt_clip.set_position(('center',0.7), relative=True).set_duration(text_duration)
            text_clips.append(txt_clip)
            start_time += text_duration  # Update start_time for the next text clip
    
    # Composite the text clips on the cropped video
    video_with_text = mp.CompositeVideoClip([video] + text_clips)
    video_with_text.write_videofile(output_file, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True, fps=video.fps, threads=4)
                

def get_text(input_file, recognizer, lang):
    """Creates speech test file from the input video file."""
    video = mp.VideoFileClip(input_file) 
  
    # Extracting audio from video file
    audio_file = video.audio 
    audio_file.write_audiofile("temp.wav") 
    global audio_duration 
    audio_duration = audio_file.duration

    r = sr.Recognizer() 

    with sr.AudioFile("temp.wav") as source: 
        voice_data = r.record(source) 

    try:
        if recognizer == "google":
            # Using google to recognize audio 
            text = r.recognize_google(voice_data, language=lang)
            os.remove("temp.wav")
            return text
        elif recognizer == "whisper":
            # Using whisper to recognize audio 
            if lang == "en-GB":
                text = r.recognize_whisper(voice_data, language="en")
            elif lang == "tr-TR":
                text = r.recognize_whisper(voice_data, language="tr")
            os.remove("temp.wav")
            return text
    except Exception as e:
        os.remove("temp.wav")
        print(f"Error: {e}")
        sys.exit(1)
    
def parse_text_to_words(text: str) -> list:
    """
    Takes a text as an input and parses it according to the number of words. 
    For each 8 words, creates a new array item and returns an array. 
    """
    words = text.split()  # Split text into words
    return words