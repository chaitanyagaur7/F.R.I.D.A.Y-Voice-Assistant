import os
import speech_recognition as sr
import win32com.client
import datetime
import openai
from config import apikey

speaker = win32com.client.Dispatch("SAPI.spVoice")
chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Boss {query}\n F.R.I.D.A.Y: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"Response to : {prompt} \n -----------------------\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
        f.write(text)


def say(text):
    speaker.speak(text)
def take_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            query = r.recognize_google(audio, language="en-in")
            print(f"User said {query}")
            return query
        except Exception as e:
            return "Sorry, I dont understand what you say?"

if __name__ == '__main__':
    print('PyCharm')
    say("Hello Sir, I am FRIDAY")
    while True:
        text = take_voice()
        print("You mean : ",text)
        if "the time" in text:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir, THE CURRENT TIME IS {strfTime}")
        if "thank you " in text:
            say(f"Sir, it was my duty")
        elif "Hey Friday".lower() in text.lower():
            ai(prompt=text)

        elif "FRIDAY Quit".lower() in text.lower():
            exit()

        elif "reset chat".lower() in text.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(text)
