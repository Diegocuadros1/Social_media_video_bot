from creator.generate_content import create_prompt
from creator.tts import speech_generator
from creator.create_video import create_video

#intro
print("Welcome to my automated trivia maker!!")
language = input("What language do you want to create the trivia in?: ")
background = "./background_videos/" + language + ".mp4"

#generate prompt and assigning it to questions
questions = create_prompt(language)

# generate tts for the trivia questions
generate_speech = 'y'
while generate_speech == 'y':
    speech_generator(questions, language)
    generate_speech = input("redo this trivia tts? y/n: ")

#combine the video and save it to the output
print("Generating Content Video")
create_video(questions, language)







