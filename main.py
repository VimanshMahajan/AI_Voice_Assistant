import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import openai
import os
from config import apikey


chatStr = ""


def say(text):

    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    engine.say(text)
    engine.runAndWait()


def take_command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1.5
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            say("Sorry, I did not get that. Please repeat.")
            return ""
        except sr.RequestError as e:
            say(f"Could not request results {e}")
            return ""


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI assistant: {prompt[24:]} \n\n****************************\n\n"
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    # requesting the response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=conversation_history,
        max_tokens=2500
    )

    # Extract and return the AI-generated text from the response
    generated_text = response['choices'][0]['message']['content']
    text += response['choices'][0]['message']['content']
    if not os.path.exists("openai"):
        os.mkdir("openai")
    with open(f"openai/{''.join(prompt.split('intelligence')[1:])}.txt", "w") as f:
        f.write(text)
    return generated_text


def chat(prompt):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {prompt}\n Jarvis: "
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": chatStr}  # Use the provided prompt here
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=conversation_history,
        max_tokens=2500
    )
    say(response['choices'][0]['message']['content'])
    chatStr += f"{response['choices'][0]['message']['content']}\n"
    return response["choices"][0]["message"]["content"]


if __name__ == "__main__":
    jarvis_active = False  # Flag to indicate if Jarvis is active

    while True:
        query = take_command().lower()

        if "jarvis ai".lower() in query.lower():
            say("Jarvis A.I. activated")
            jarvis_active = True
            continue

        if not jarvis_active:
            continue  # Skip processing commands if Jarvis is not activated

        if "Jarvis sleep".lower() in query.lower():
            say("Going to sleep. Goodbye!")
            jarvis_active = False
            continue

        # Execute commands only if Jarvis is active
        if "open" in query:
            flag = False
            sites = [["youtube", "https://www.youtube.com"], ["gmail", "https://www.gmail.com"],
                     ["wikipedia", "https://en.wikipedia.com"], ["github", "https://github.com"],
                     ["whatsapp", "https://web.whatsapp.com"]]
            for site in sites:
                if f"open {site[0]}" in query:
                    say(f"opening {site[0]}")
                    flag = True
                    webbrowser.open(site[1])
            if not flag:
                say("Sorry, I don't know that website")

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour} hours and {minute} minutes")

        elif "see you later" in query:
            say("Until next time, bye!")
            break

        elif "artificial intelligence" in query:
            ai(query)
            say("Query processed and recorded in the storage folder")

        elif "reset chat" in query:
            say("Chat reset")
            chatStr = ""

        else:
            chat(query)
