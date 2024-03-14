import streamlit as st
from pydub import AudioSegment 

import os 
import shutil 
import openai

client = openai
def speech_to_text(path_name:str):
    with open(path_name,'rb') as audio_bytes:
        transcription = client.audio.transcriptions.create(
            file=audio_bytes,
            model='whisper-1',
        )

        response_text = transcription.text 

        return response_text

        # return  choice(["helo",'how','are','you','i am','fine'])

def file_to_chunks(upload_file_path):
    if upload_file_path:
        with open(upload_file_path.name,'wb') as f:
            f.write(upload_file_path.getbuffer())

    path = './projects'
    os.makedirs(path)

    audio_list = []
    text = []

    audio = AudioSegment.from_file(upload_file_path.name)
    total_len = len(audio) 
    one_minutes = 1000*60 #converted sencond in one minutes

    for index,i in enumerate(range(0,total_len,one_minutes)): 
        trimed_audio = audio[i:i+one_minutes] 
        # number = int(i/one_minutes) 
        file_name = f'output{index}.mp3' 
        outputfile  = os.path.join(path,file_name) 
        trimed_audio.export(outputfile) 
        audio_list.append(file_name) 

    for name in audio_list:
            response = speech_to_text(f"{path}/{name}")
            text.append(response)

   
    shutil.rmtree(path)
    os.remove(upload_file_path.name)

    text_result  = ' '.join(text)

    return text_result



def text_to_speech(text:str,voice_type:str="alloy"):
    max_length = 4096 
    chunks = [text[i:i+max_length] for i in range(0,len(text),max_length)]
    audio_files = []
    audio_file_name = []
    for i,chunk in enumerate(chunks):
        try:
            response = client.audio.speech.create(
                model="tts-1",
                input=chunk,
                voice=voice_type,
            )

            speech_file_path = f"chunk_{i}.mp3"
            audio_file_name.append(speech_file_path)
            response.stream_to_file(speech_file_path)
            audio_files.append(AudioSegment.from_mp3(speech_file_path))
        except Exception as e:
            st.error(f"Error in text-to-speech conversion for chunk {i}: {e}")
            return None 
    
    compined = AudioSegment.empty()
    for i in audio_files:
        compined += i 
    for audio_file in audio_file_name:
        os.remove(audio_file)
    combined_file_path = "combined_speech.mp3"
    compined.export(combined_file_path,format="mp3")
    return combined_file_path 
