Requirements for operating the social media video bot:

Translator API key: Rapid API
https://rapidapi.com/gatzuma/api/deep-translate1

Text to speech API: Elevenlabs 
https://elevenlabs.io/

make sure you put your api keys in a .env file and name the translator API key TRANSLATOR_API_KEY and the Elevenlabs key ELEVENLABS_API

Can only operate 10,000 characters per month with the free versino

pick your text to speech person as anyone in elevenlabs, then grab the persons ID and paste it on the top of the desired name in the tts.py file. Example below:
english = "<Paste_Your_ID_Here>"


run the code and install the required packages in requirements.txt

If you would like you can add your own custom background images to change the style of the background (make sure it is 1080 x 1900 for it to work as a reel / tiktok 
- Make sure that your file is in the folder called backgrounds and make sure that your video is an mp4 and it is the named the language you are translating to.

If you would like to change the words that are randomly generated, you can change the file called data.txt. Every line is a different word that can be translated

If you would like to change the amount of questions being run, you can change the AMOUNT_OF_QUESTIONS variable at the top of generate_content.py
- Keep in mind that moviepy concatination is extremely slow, depending on the amount of questions 10 questions could take over an hour

Answer the series of questions to generate your questions. When your questions are finished, look inside of the tts output folder and try to find out if the voice matches the required voice that you want. If it doesn't you can regenerate the text to speech. Once text to speech is approved, it will generate the video, and it will output as a video titled final_video.mp4

Run main.py

A rundown on how the program works
 - There are three main files in the program: create_video.py, generate_content.py, and tts.py

 - generate content runs first and creates the functions necessary to generate the trivia content, returning the content in an array with different questions in each array
When you generate a question, words from data.txt will be randomly selected and chosen as a word. Then these words will be translated with the desired language and then 
placed on a b c d, the word with the matching translation to the word from the question is the right answer

 - tts.py creates the functions necessary to create a text to speech from the trivia content that was made previously

 - create_video combines the text to speech, the background video, and gets the questions and combines them all in a video with moviepy.



