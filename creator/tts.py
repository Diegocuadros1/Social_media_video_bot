import os
from dotenv import load_dotenv
import requests


load_dotenv()

CHUNK_SIZE = 1024

english = "joO0GIEMz4TeN9ahxFcc" #Kevin - Smooth and Emotive
japanese = "j210dv0vWm7fCknyQpbA" #Hinata
spanish = "Nh2zY9kknu6z4pZy6FhD" #David Martin


api_key = os.getenv('ELEVENLABS_API')

#using API to generate the content
def generate_tts(content, language, filename):

    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{language}"

    print('generating tts...')

    headers = {
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    payload = {
        "text": content,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    speech = requests.post(tts_url, json=payload, headers=headers)

    #convert tts
    with open(f'./creator/tts_output/{filename}.mp3', 'wb') as audio_file:
        for chunk in speech.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                audio_file.write(chunk)



def speech_generator(content, language):

    tts_language = find_language(language)
    
    if not tts_language:
        return False
    
    for item in content:
        
        #generating speech for the question being asked
        question = item[0]
        q_num = content.index(item)
        generate_tts(question, english, f"question{q_num + 1}")

        #generating speech for the answer
        answer = item[5]
        generate_tts(answer, tts_language, f"answer{q_num + 1}")

    return True

def find_language(language):
    if language == "spanish":
        return spanish
    if language == "japanese":
        return japanese
    
    else: 
        print("No language found for tts")

        ignore_tts = input("Ignore tts for video? y/n: ")

        if ignore_tts == 'y':
            return False



