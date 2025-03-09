import speech_recognition as sr
import webbrowser
import pyttsx3
import datetime
import os
import random
import time
from ai import client
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()



def chat(query):
    chats = ""
    
    OpenAI.api_key = 'OPENAI_API_KEY'
    chats += f"me : {query}\n Leviathan: "  
   # print(chats)
    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=[{"role": "user", "content": chats}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )
        saying = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                saying += f"{chunk.choices[0].delta.content}"  
                chats  += f"{chunk.choices[0].delta.content}"
        
        saying = clean_text(saying)
        say(saying) 

        if not os.path.exists("OpenAi"):
            os.mkdir("OpenAi")

        with open(f"OpenAi/{query}.txt", "w") as file:
            file.write(saying)
        #say(saying)
        print(chats) 
    except Exception as e:
        print(f"Error during AI request: {e}")

def clean_text(text):
    cleaned_text = text.replace('*', '')  
    return cleaned_text

def ai(prompt):
    try:
        completion = client.chat.completions.create(
            model="meta/llama-3.3-70b-instruct",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )

        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")

        if not os.path.exists("OpenAi"):
            os.mkdir("OpenAi")

        with open(f"OpenAi/{prompt}.txt", "w") as file:
            file.write(chunk.choices[0].delta.content)

    except Exception as e:
        print(f"Error during AI request: {e}")


def say(text):
    engine = pyttsx3.init()
   # engine.say(text)
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.5
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        return query
    except Exception as e:
        return "Some error has occurred. Sorry for the inconvenience."


if __name__ == '__main__':
    print('Pycharm')
    say("Hello, I'm Hailey and I'm here to help you!!")

    print("How can I help you?")
    query = takecommand()

    if not query.strip():
        print("No valid input received. Please try again.")
        say("Sorry, I couldn't hear anything. Please try again.")
    else:
        sites = [
            ["youtube", "https://youtube.com"],
            ["google", "https://google.com"],
            ["facebook", "https://facebook.com"],
            ["instagram", "https://instagram.com"],
            ["wikipedia", "https://wikipedia.com"],
            ["spotify", "https://spotify.com"],
            ["twitter", "https://twitter.com"],
            ["linkedin", "https://linkedin.com"],
            ["github", "https://github.com"],
            ["amazon", "https://amazon.com"],
            ["flipkart", "https://flipkart.com"],
            ["snapdeal", "https://snapdeal.com"],
            ["myntra", "https://myntra.com"],
            ["paytm", "https://paytm.com"],
            ["udemy", "https://udemy.com"],
            ["coursera", "https://coursera.com"],
            ["geeksforgeeks", "https://geeksforgeeks.com"],
            ["hackerrank", "https://hackerrank.com"],
            ["hackerearth", "https://hackerearth.com"],
            ["codechef", "https://codechef.com"],
            ["codeforces", "https://codeforces.com"],
            ["leetcode", "https://leetcode.com"],
            ["gfg", "https://gfg.com"],
            ["stackoverflow", "https://stackoverflow.com"],
            ["w3schools", "https://w3schools.com"],
            ["tutorialspoint", "https://tutorialspoint.com"],
            ["javatpoint", "https://javatpoint.com"]
        ]

        for site in sites:
            if site[0] in query.lower():
                say(f"Opening {site[0]}")
                webbrowser.open(site[1])

        if 'games' in query:
            webbrowser.open("https://poki.com")
        elif 'music' in query:
            webbrowser.open("https://spotify.com")
        elif 'the time' in query:
            strftime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"The time is {strftime}")
        elif "open ai" in query.lower():
            prompt = query
            ai(prompt)
        else:
            chat(query)
