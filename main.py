import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import os
import re
import webbrowser


listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


custom_commands = {
    re.compile(".*(your name).*"): "My name is Alexa!",
    re.compile(".*(your purpose).*"): "I exist to assist you with various tasks!"
}

def talk(text):
    """Speak the provided text."""
    engine.say(text)
    engine.runAndWait()

def take_command(timeout=1, phrase_time_limit=4):
    """Listen for a command from the user."""
    command = ""
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = listener.recognize_google(voice)
            command = command.lower()
    except sr.UnknownValueError:
        talk("Sorry, I did not understand that.")
    except sr.RequestError:
        talk("Sorry, my speech service is down.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return command

def write_to_notepad(text):
    """Write the provided text to a notepad file."""
    with open("alexa_notepad.txt", "a") as file:
        file.write(text + " ")
    os.system("notepad.exe alexa_notepad.txt")

def calculate_expression(expression):
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        talk(f"The result is {result}")
    except Exception as e:
        talk("Sorry, I couldn't calculate that. Please try again.")

def search_web(query):
    """Search the web using the provided query."""
    talk(f"Searching for {query}")
    webbrowser.open(f"https://www.google.com/search?q={query}")

def run_alexa():
    """Run the main Alexa functionality."""
    command = take_command()
    print(f"Command recognized: {command}")

    
    for pattern, response in custom_commands.items():
        if pattern.match(command):
            talk(response)
            return False 

    if 'play' in command:
        song = command.replace('play', '').strip()
        talk('Playing ' + song)
        pywhatkit.playonyt(song)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('Current time is ' + time)
    elif 'who the heck is' in command:
        person = command.replace('who the heck is', '').strip()
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)
    elif 'date' in command:
        talk('Sorry, I have a headache.')
    elif 'are you single' in command:
        talk('I am in a relationship with WiFi.')
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'go to notepad' in command:
        talk("Start speaking, and I will write to the notepad. Say 'stop writing' to finish.")
        while True:
            note_text = take_command(timeout=10)
            if 'stop writing' in note_text:
                talk("Stopped writing to notepad.")
                break
            if note_text:
                write_to_notepad(note_text)
    elif 'calculate' in command:
        expression = command.replace('calculate', '').strip()
        talk(f"Calculating {expression}")
        calculate_expression(expression)

    elif 'search' in command:
            search_query = command.replace('search', '').strip()
            search_web(search_query)

    elif 'stop listening' in command or 'goodbye' in command:
        talk("Goodbye! and MissYou!")
        return True 
    else:
        talk('Please say the command again.')
    
    return False  


while True:
    if run_alexa():
        break
