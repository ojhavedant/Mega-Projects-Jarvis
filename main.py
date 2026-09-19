import speech_recognition as sr 
import webbrowser
import pyttsx3
import musicLibrary #Favourate songs written in a certain folder in dictionary format with there youtube links given to them
import subprocess
import requests
import os
from dotenv import load_dotenv
from google import genai
import urllib.request
import urllib.parse
import re

load_dotenv()

#Fetch the secure api key
newsapi = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
recognizer = sr.Recognizer()
client = genai.Client(api_key=GEMINI_API_KEY)
chat_session = client.chats.create(model="gemini-3.6-flash")

BRAVE_PATH=r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
webbrowser.register('brave',None,webbrowser.BackgroundBrowser(BRAVE_PATH))

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()

def open_in_brave(url):
    try:
        webbrowser.get('brave').open(url)
    except (webbrowser.Error, OSError, FileNotFoundError):
        print('Brave not found. Trying Chrome...')
        webbrowser.open(url)

def open_in_brave_private(url):
    try:
        speak("Opening in Brave Private")
        # The raw string (r) handles the backslashes safely
        path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
        # Popen sends the exact instructions directly to Windows
        subprocess.Popen([path, "--incognito", url])
    except Exception as e:
        print('Brave not found. Trying Chrome...')
        webbrowser.open(url)

def processCommand(c):
    if "open google" in c.lower():
        open_in_brave("https://www.google.com")
    elif "open youtube private" in c.lower() or "open youtube incognito" in c.lower():
        open_in_brave_private("https://www.youtube.com")
    elif "open youtube" in c.lower():
        open_in_brave("https://www.youtube.com")
    elif "open facebook" in c.lower():
        open_in_brave("https://www.facebook.com")
    elif "open twitter" in c.lower():
        open_in_brave("https://www.twitter.com")
    elif "open instagram" in c.lower():
        open_in_brave("https://www.instagram.com")
    elif "open reddit" in c.lower():
        open_in_brave("https://www.reddit.com")
    elif "open whatsapp" in c.lower():
        open_in_brave("https://web.whatsapp.com")
    elif "open gmail" in c.lower():
        open_in_brave("https://mail.google.com")
    elif "open linkedin" in c.lower():
        open_in_brave("https://www.linkedin.com")
    elif "open stackoverflow" in c.lower():
        open_in_brave("https://stackoverflow.com")
    elif "open wikipedia" in c.lower():
        open_in_brave("https://en.wikipedia.org")
    elif "open spotify" in c.lower():
        open_in_brave("https://open.spotify.com")
    elif "open soundcloud" in c.lower():
        open_in_brave("https://soundcloud.com")
    elif "open apple music" in c.lower():
        open_in_brave("https://music.apple.com")
    elif "open youtube music" in c.lower():
        open_in_brave("https://music.youtube.com")
    elif "open netflix" in c.lower():
        open_in_brave("https://www.netflix.com")
    elif "open shazam" in c.lower():
        open_in_brave("https://www.shazam.com")
    elif "open heritage mail" in c.lower():
        open_in_brave("https://mail.google.com/mail/u/1/")
    elif "open playlist" in c.lower():
        open_in_brave(musicLibrary.musicList["Playlist"])
    elif "open private" in c.lower():
        open_in_brave_private("https://www.google.com")
    elif c.lower().startswith("play "):
        song=c.lower().split(" ")
        if len(song)==2:
            speak("Playing "+song[1])
            if song[1] in musicLibrary.musicList:
                open_in_brave_private(musicLibrary.musicList[song[1]])
            else:
                speak(f"Searching YouTube for {song[1]}")
                try:
                    # Format the search query safely (e.g., turns spaces into + signs)
                    query_string = urllib.parse.urlencode({"search_query": song[1]})
                    html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
                    
                    # Scan the YouTube source code for the first 11-character video ID
                    search_results = re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html_content.read().decode())
                    
                    if search_results:
                        song_url = "https://www.youtube.com/watch?v=" + search_results[0]
                        open_in_brave_private(song_url)
                    else:
                        speak("I couldn't find that song on YouTube.")
                except Exception as e:
                    print(f"YouTube search error: {e}")
                    speak("I encountered an error searching for that song.")
        else:
            song_name=""
            for i in range(1,len(song)):
                if i!=len(song)-1:
                    song_name+=song[i]+" "
                else:
                    song_name+=song[i]
            speak("Playing "+song_name)
            if song_name in musicLibrary.musicList:
                open_in_brave_private(musicLibrary.musicList[song_name])
            else:
                speak(f"Searching YouTube for {song_name}")
                try:
                    # Format the search query safely (e.g., turns spaces into + signs)
                    query_string = urllib.parse.urlencode({"search_query": song_name})
                    html_content = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)
                    
                    # Scan the YouTube source code for the first 11-character video ID
                    search_results = re.findall(r'watch\?v=([a-zA-Z0-9_-]{11})', html_content.read().decode())
                    
                    if search_results:
                        song_url = "https://www.youtube.com/watch?v=" + search_results[0]
                        open_in_brave_private(song_url)
                    else:
                        speak("I couldn't find that song on YouTube.")
                except Exception as e:
                    print(f"YouTube search error: {e}")
                    speak("I encountered an error searching for that song.")

    elif "news" in c.lower():
        if "india" in c.lower():
            speak("India News")
            r = requests.get(f"https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey={newsapi}")
            if r.status_code==200:
                #Parse the JSON response
                data=r.json()

                #Extract the articles 
                articles=data.get('articles',[])
                #Prints the headlines
                for article in articles:
                    speak(article['title'])
        elif "usa" in c.lower():
            speak("USA News")
            r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
            if r.status_code==200:
                #Parse the JSON response
                data=r.json()

                #Extract the articles 
                articles=data.get('articles',[])
                if not articles:
                    speak("I couldn't find any articles for India right now.")
                #Prints the headlines
                else:
                    for article in articles:
                        speak(article['title'])

    else:
        #Let gemini handle this job
        try:
            # Force a concise response suited for a voice assistant
            response = chat_session.send_message(c)
            
            # Strip out markdown symbols so pyttsx3 doesn't read "asterisk asterisk" out loud
            clean_text = response.text.replace("*", "").replace("#", "")
            
            print(f"Jarvis: {clean_text}")
            speak(clean_text)
        except Exception as e:
            print(f"Gemini API Error: {e}")
            speak("Sorry, I am having trouble connecting to the Gemini network right now.")
        
if __name__=="__main__":
    speak("Initializing Jarvis....")
    while True:
        #Listen to the wake word Jarvis
        #Obtain audio from the microphone
        r=sr.Recognizer()
        
        print("Recognizing...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source,duration=1)
                print("Listening...")   
                audio=r.listen(source,timeout=3,phrase_time_limit=3)
            word=r.recognize_google(audio)

            if "jarvis" in word.lower():
                speak("Jarvis is awake")
                #Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Activated")
                    audio=r.listen(source)
                    command=r.recognize_google(audio)
                    processCommand(command)
        except Exception as e:
            print("Error; {0}".format(e))