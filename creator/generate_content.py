from dotenv import load_dotenv
import os
import random
import requests
from langcodes import Language
from unidecode import unidecode

load_dotenv()

#translator API
translator_api = 'https://deep-translate1.p.rapidapi.com/language/translate/v2'

#Global Varibale for Amount of questions on the trivia quiz
AMOUNT_OF_QUESTIONS = 3

def create_prompt(language):

    personal_question = input("Would you like to leave a personal trivia question? y/n: ")

    #initializing empty array of trivia questions. Max is 5
    trivia_questions = []

    if personal_question == "y":
        i = 0
        while i < AMOUNT_OF_QUESTIONS:
            question = input("Fill in the blank: How do you say ______ in " + language + "? ")
            question = translate_into_game(question, language)
            
            answer = input("Would you like to add another custom question? y/n ")

            if answer == "y":
                i += 1
                trivia_questions.extend(question)
                continue
            else:
                trivia_questions.extend(question)
                trivia_questions.extend(generate_content(language, AMOUNT_OF_QUESTIONS - 1 - i))
                break

    else:
        trivia_questions = generate_content(language, AMOUNT_OF_QUESTIONS)

    print(trivia_questions)

    for i in range(len(trivia_questions)):
        print('Trivia Question ' + str(i + 1) + ': ', trivia_questions[i][0])
        print("A. ", trivia_questions[i][1])
        print("B. ", trivia_questions[i][2])
        print("C. ", trivia_questions[i][3])
        print("D. ", trivia_questions[i][4])
        print("Correct Answer: ", trivia_questions[i][5])

    restart = input("Redo this trivia quiz? y/n: ")

    if restart == "y":
        create_prompt(language)

    else:
        return trivia_questions

#translating english words into the specified language
def translate(word, language):
    #translating language into iso 369 conversion
    language = Language.find(language).to_tag()

    #assigning headers & data
    headers = {
        'X-RapidAPI-Key': os.getenv('TRANSLATOR_API_KEY'),
        'X-RapidAPI-Host': 'deep-translate1.p.rapidapi.com',
        'Content-Type': 'application/json'
    }
    data = {
        "q": word,
        "source": "en",
        "target": language,
    }

    #response data
    response = requests.post(translator_api, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()['data']['translations']['translatedText']

    else:
        print("An error has occurred, Status Code: ", response.status_code, response.json())


#generates a trivia quiz question with abcd and the answer
def generate_content(language, amt):
    
    content = []

    for i in range(amt):

        state = ""
        while state != "y":
            word = find_random_word()
            

            either_or = random.randint(0, 1)
            question = [f"What is the {language} word for '{word}'?", f"How do you say '{word}' in {language}?"]
            question = question[either_or]

            print(question)

            word = unidecode(translate(word, language))
            word1 = unidecode(translate(find_random_word(), language))
            word2 = unidecode(translate(find_random_word(), language))
            word3 = unidecode(translate(find_random_word(), language))

            #randomly assigning a word to a b c or d
            answers = [word, word1, word2, word3]
            random.shuffle(answers)

            print("A. ", answers[0])
            print("B. ", answers[1])
            print("C. ", answers[2])
            print("D. ", answers[3])
            print("Real Answer: ", word)

            state = input("Continue with this question? y/n: ")
            if state == 'y':
                content.append([question, answers[0], answers[1], answers[2], answers[3], word])

    return(content)


def translate_into_game(word_input, language):

    content = []

    question = f"How do you say '{word_input}' in {language}? "
    print(question)

    #translating words
    word = unidecode(translate(word_input, language))
    word1 = unidecode(translate(find_random_word(), language))
    word2 = unidecode(translate(find_random_word(), language))
    word3 = unidecode(translate(find_random_word(), language))

    #shuffling words
    answers = [word, word1, word2, word3]
    random.shuffle(answers)

    print("A. ", answers[0])
    print("B. ", answers[1])
    print("C. ", answers[2])
    print("D. ", answers[3])
    print("Answer: ", word)

    cont = input("Continue with this question? y/n: ")
    
    if cont != 'y':
        translate_into_game(word_input, language)

    content.append([question, answers[0], answers[1], answers[2], answers[3], word])

    return content


def find_random_word():
    random_line = random.randint(1, 350)
    counter = 0
    with open('./data.txt', 'r') as file:
        for line in file:
            counter += 1
            if counter == random_line:
                return line.strip()
            


#word2len = 2 word1len = 2 
#[a, p, b, q, ]
#