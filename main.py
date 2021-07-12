#Author: Cem Gumulcineli
import speech_recognition as sr     #pip install SpeechRecognition
import playsound                    #pip install playsound
from gtts import gTTS               #pip install gTTS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
import sys, os, random, time, webbrowser
from datetime import datetime


'''
Implemented commands:
Current date    ex. What is the current date
Current time    ex. What is the current time
Search/Search for anything on google - different ways of saying it - Search dogs, Search the internet for dogs, Search for dogs
Find location - with Google Maps    ex. Find location Los Angeles California
Ask for the assistants name     ex. What is your name?
Exit - to stop the program and exit
'''


recognizer = sr.Recognizer()  #initialize recognizer
assistant_questions = ["What else can I do for you", "How else can I help you", "Anything else I can do", "Any other questions", "Anything else"]



def get_user_voice():
    with sr.Microphone() as source:
        voice_data = "" # initialize voice data
        try:
            audio = recognizer.listen(source,  timeout=3)   # store what was said into the microphone here, as audio
        except sr.WaitTimeoutError:
            assistant_voice("Sorry, I did not hear any sound from your microphone, so please try again later.")
            sys.exit()
        try:
            voice_data = recognizer.recognize_google(audio)     # speech recognition on audio, see if audio can be turned into text
            print("User: " + voice_data)
        except sr.UnknownValueError: 
            assistant_voice
            ("Sorry, can't make out what you are trying to say, please try again.")
            sys.exit()
        except sr.RequestError: 
            assistant_voice("Sorry, the service is unavailable right now.")
            sys.exit()
        


    return voice_data

def assistant_response(voice_data):
    if "your name" in voice_data:   # if the person asks for the name of the assistant
         assistant_voice("This information has not been decided yet.")
    elif "current time" in voice_data:  # if the person asks for the current time (12 hr clock, can be adjusted to 24 hr)
         assistant_voice(get_datetime_info().strftime("The time is %I:%M %p"))
    elif "current date" in voice_data: # if the person asks for the current date
         assistant_voice(get_datetime_info().strftime("Today is %B %d, %Y"))
    elif "search" in voice_data: # the term search or search for must be used for a google search
        if "for" in voice_data:
            search_query = voice_data[voice_data.index("for") + 4:]   # change starting index so the browser search query is caught properly ex. search the internet for cats, search for cats
        else:
            search_query = voice_data[voice_data.index("search") + 7:]    # change starting index so the browser search query is caught properly ex. search cats

        url = "https://google.com/search?q=" + search_query     # making a google search with the search query from user microphone
        webbrowser.get().open(url)
        assistant_voice("Here is what I found for " + search_query)
    elif "find location" in voice_data:
        search_query = voice_data[voice_data.index("location") + 9:]
        url = "https://google.com/maps/place/" + search_query     # making a google maps search with the search query from user microphone
        url = url.replace(" ", "+")
        webbrowser.get().open(url)
        assistant_voice("Here is what I found for " + search_query)
    elif "exit" in voice_data:
        assistant_voice("See you next time!")
        sys.exit()


def assistant_voice(input_string):      # turn a string into an audio file where the assistant speaks to you, delete the file right after use
    tts = gTTS(text=input_string, lang="en")
    rnd = random.randint(1, 10000)
    audio_file = "audio_" + str(rnd) + ".mp3"   # audio file is made
    tts.save(audio_file)
    playsound.playsound((audio_file))   # the sound is played
    print(input_string)
    os.remove(audio_file)   # audio file is deleted


def get_datetime_info():
    return datetime.now()  # 2021-07-08 21:18:03.048202 -> is in the format yr-month-day 24 hr clock time ---- https://docs.python.org/3/library/time.html for % format


if __name__ == '__main__':
    assistant_voice("Welcome, how can I help you?")
    while True:
        vd = get_user_voice()
        assistant_response(vd)
        time.sleep(1)
        choice_number = len(assistant_questions) - 1
        assistant_voice(assistant_questions[random.randint(1, choice_number)])  # randomly choose one of the pre-written assistant follow up questions
