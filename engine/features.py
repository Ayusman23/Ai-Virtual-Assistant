import json
import os
from shlex import quote
import sqlite3
import struct
import subprocess
import time
import webbrowser
import eel
import pyaudio
import pyautogui
from .command import speak
from .config import ASSISTANT_NAME, LLM_KEY, PICOVOICE_ACCESS_KEY
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine
from datetime import datetime
import pygame
import requests
import wikipedia
import wolframalpha
from ddgs import DDGS
import git
import google.generativeai as genai
from .helper import extract_yt_term, markdown_to_text, remove_words, ADB_PATH

pygame.mixer.init()

# --- API KEYS ---
OPENWEATHER_KEY = "bd5e378503939ddaee76f12ad7a97608"
NEWS_API_KEY = "63c7b53f7f1172629f7dc617033961bf"
WOLFRAM_APP_ID = "3H4296-5YPAGQUJK7"

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Global context to store brief info about uploaded files or folders
SESSION_CONTEXT = {
    "current_path": None,
    "last_analysis": None,
    "file_metadata": {}
}

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    try:
        pygame.mixer.music.load(music_dir)
        pygame.mixer.music.play()
        # You might need to add a small sleep to ensure the file starts playing before the function exits
        time.sleep(1) 
    except Exception as e:
        print(f"Error playing sound with pygame: {e}")

    
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

       

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(access_key=PICOVOICE_ACCESS_KEY, keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

# chat bot 
def chatBot(query):
    user_input = query.lower()
    cookie_path = os.path.join(os.path.dirname(__file__), "cookies.json")
    chatbot = hugchat.ChatBot(cookie_path=cookie_path)
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)

import google.generativeai as genai
def geminai(query):
    try:
        query = query.replace(ASSISTANT_NAME, "")
        query = query.replace("search", "")
        
        genai.configure(api_key=LLM_KEY)
        model = genai.GenerativeModel("models/gemini-2.0-flash") # Verified model

        # Define prompt with current time and assistant persona
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prompt = f"""
        System: Current date and time is {current_time}. 
        You are {ASSISTANT_NAME}, a highly advanced AI voice assistant.
        Your goal is to provide precise, helpful, and high-quality answers.
        If a user asks for a calculation or complex problem, solve it with full logic.
        Be conversational but concise. User query: {query}
        """

        # Add context if available
        if SESSION_CONTEXT["last_analysis"]:
            prompt = f"Context from previous analysis: {SESSION_CONTEXT['last_analysis']}\n\n" + prompt

        response = model.generate_content(prompt)
        filter_text = markdown_to_text(response.text)
        speak(filter_text)
    except Exception as e:
        print("Gemini Error:", e)
        speak("I am having trouble connecting to my brain.")

# Settings Modal 



# Assistant name
@eel.expose
def assistantName():
    name = ASSISTANT_NAME
    return name


@eel.expose
def personalInfo():
    try:
        cursor.execute("SELECT * FROM info")
        results = cursor.fetchall()
        jsonArr = json.dumps(results[0])
        eel.getData(jsonArr)
        return 1    
    except:
        print("no data")


@eel.expose
def updatePersonalInfo(name, designation, mobileno, email, city):
    cursor.execute("SELECT COUNT(*) FROM info")
    count = cursor.fetchone()[0]

    if count > 0:
        # Update existing record
        cursor.execute(
            '''UPDATE info 
               SET name=?, designation=?, mobileno=?, email=?, city=?''',
            (name, designation, mobileno, email, city)
        )
    else:
        # Insert new record if no data exists
        cursor.execute(
            '''INSERT INTO info (name, designation, mobileno, email, city) 
               VALUES (?, ?, ?, ?, ?)''',
            (name, designation, mobileno, email, city)
        )

    con.commit()
    personalInfo()
    return 1



@eel.expose
def displaySysCommand():
    cursor.execute("SELECT * FROM sys_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displaySysCommand(jsonArr)
    return 1


@eel.expose
def deleteSysCommand(id):
    cursor.execute("DELETE FROM sys_command WHERE id = ?", (id,))
    con.commit()


@eel.expose
def addSysCommand(key, value):
    cursor.execute(
        '''INSERT INTO sys_command VALUES (?, ?, ?)''', (None,key, value))
    con.commit()


@eel.expose
def displayWebCommand():
    cursor.execute("SELECT * FROM web_command")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayWebCommand(jsonArr)
    return 1


@eel.expose
def addWebCommand(key, value):
    cursor.execute(
        '''INSERT INTO web_command VALUES (?, ?, ?)''', (None, key, value))
    con.commit()


@eel.expose
def deleteWebCommand(id):
    cursor.execute("DELETE FROM web_command WHERE Id = ?", (id,))
    con.commit()


@eel.expose
def displayPhoneBookCommand():
    cursor.execute("SELECT * FROM contacts")
    results = cursor.fetchall()
    jsonArr = json.dumps(results)
    eel.displayPhoneBookCommand(jsonArr)
    return 1


@eel.expose
def deletePhoneBookCommand(id):
    cursor.execute("DELETE FROM contacts WHERE Id = ?", (id,))
    con.commit()


@eel.expose
def InsertContacts(Name, MobileNo, Email, City):
    cursor.execute(
        '''INSERT INTO contacts VALUES (?, ?, ?, ?, ?)''', (None,Name, MobileNo, Email, City))
    con.commit()

# --- NEW INTEGRATED FEATURES ---



class RealTimeData:
    @staticmethod
    def get_weather(city):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
            res = requests.get(url).json()
            if res.get("cod") != "404":
                temp = res["main"]["temp"]
                desc = res["weather"][0]["description"]
                return f"Weather in {city}: {temp}°C, {desc}."
            return "City not found."
        except: 
            return "Internet connection error."

    @staticmethod
    def get_news():
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
            res = requests.get(url).json()
            articles = res.get('articles', [])[:3]
            headlines = [art['title'] for art in articles]
            return "Top Headlines: " + " | ".join(headlines)
        except: 
            return "Could not fetch news."

    @staticmethod
    def google_search(query):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=3))
                if results:
                    summary = ""
                    for res in results:
                        summary += f"- {res['title']}: {res['body']}\n"
                    return summary
            return "No search results found."
        except Exception as e:
            print(f"Search Error: {e}")
            return "Search failed."

    @staticmethod
    def get_wiki(query):
        try: 
            return wikipedia.summary(query, sentences=2)
        except: 
            return "Wikipedia entry not found."

    @staticmethod
    def ask_math(query):
        try:
            client = wolframalpha.Client(WOLFRAM_APP_ID)
            res = client.query(query)
            return next(res.results).text
        except: 
            return "I couldn't calculate that."

class AutoUpdater:
    @staticmethod
    def check_and_update():
        try:
            speak("Checking for updates...")
            repo = git.Repo(os.getcwd())
            origin = repo.remotes.origin
            origin.fetch()
            head = repo.head.ref
            tracking = head.tracking_branch()
            
            if tracking and head.commit != tracking.commit:
                speak("New update found. Downloading now...")
                origin.pull()
                speak("Update downloaded. Please restart the application.")
                return True
            else:
                speak("System is up to date.")
                return False
        except Exception as e:
            print(f"Update Error: {e}")
            speak("I couldn't check for updates.")
            return False

@eel.expose
def analyzeFolder(folderName, fileList):
    """Summarizes an uploaded folder using Gemini."""
    try:
        eel.ShowWave()
        speak(f"Analyzing {folderName}. Please wait.")
        
        # Construct a detailed prompt about the file structure
        summary_prompt = f"""
        Analyze the following folder structure and explain its purpose, likely tech stack, and main functionality. 
        Folder Name: {folderName}
        Files: {', '.join(fileList[:50])}
        
        Provide a professional summary.
        """
        
        genai.configure(api_key=LLM_KEY)
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(summary_prompt)
        
        speak(f"Analysis complete for {folderName}.")
        speak(response.text)
        
        return response.text
    except Exception as e:
        print("Folder Analysis Error:", e)
        speak("I encountered an error while analyzing the folder structure.")

@eel.expose
def trainFaceRecognition():
    """Runs the training logic to improve recognition."""
    try:
        from engine.auth.face_trainer import capture_samples, train_model
        
        speak("Starting face sampling. Please look directly into the camera.")
        samples_count = capture_samples(face_id=1) # Defaulting to ID 1 for owner
        
        if samples_count > 0:
            speak(f"Captured {samples_count} samples. Now training the model.")
            success = train_model()
            if success:
                speak("Training successful! I will recognize you much better now.")
            else:
                speak("Training script failed to save the model.")
        else:
            speak("I couldn't capture any face samples. Please check your camera.")
            
    except Exception as e:
        print("Training Error:", e)
        speak("Face training process failed.")

@eel.expose
def analyzeFile(fileName, content=None):
    """Analyze an individual file."""
    try:
        eel.ShowWave()
        speak(f"Reading file {fileName}...")
        
        prompt = f"Analyze this file named '{fileName}'. Content (first 2000 chars): {content[:2000] if content else 'No text content provided.'}"
        
        genai.configure(api_key=LLM_KEY)
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        response = model.generate_content(prompt)
        
        SESSION_CONTEXT["last_analysis"] = f"User uploaded a file named '{fileName}'. Analysis: {response.text}"
        
        speak(f"File {fileName} analyzed.")
        speak(response.text)
    except Exception as e:
        print("File Analysis Error:", e)
        speak("Failed to analyze the file.")

@eel.expose
def analyzeImage(image_data, mime_type):
    """Analyze an image using multi-modal capabilities."""
    try:
        import base64
        # image_data is expected to be a base64 string from frontend
        if image_data.startswith('data:'):
            image_data = image_data.split(',')[1]
            
        eel.ShowWave()
        speak("Analyzing the image, please wait...")
        
        genai.configure(api_key=LLM_KEY)
        model = genai.GenerativeModel("models/gemini-2.0-flash")
        
        # Format for Gemini
        img_part = {
            "mime_type": mime_type,
            "data": image_data
        }
        
        response = model.generate_content(["Describe this image in detail and answer any hidden questions or text within it.", img_part])
        
        SESSION_CONTEXT["last_analysis"] = f"User uploaded an image. Description: {response.text}"
        
        speak("Image analysis complete.")
        speak(response.text)
    except Exception as e:
        print("Image Analysis Error:", e)
        speak("I couldn't process that image.")
        
def processQuery(query):
    q = query.lower()

    # 1. --- Date and Time ---
    if "time" in q:
        now = datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")
        return now
    
    if "today" in q or "date" in q or "day" in q:
        today = datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today is {today}")
        return today

    # 2. --- Weather ---
    if "weather" in q or "temperature" in q:
        city = q.replace("weather", "").replace("temperature", "").strip()
        if city == "": city = "my location"
        answer = RealTimeData.get_weather(city)
        speak(answer)
        return answer

    # 3. --- News ---
    if "news" in q:
        answer = RealTimeData.get_news()
        speak(answer)
        return answer

    # 5. --- Math & Logic ---
    math_triggers = ["solve", "calculate", "integral", "derivative", "plus", "minus", "divided by", "times", "+", "-", "*", "/", "=", "root", "factorial", "equation"]
    if any(word in q for word in math_triggers) or (q.strip() and q.strip()[-1] == '='):
        answer = RealTimeData.ask_math(q)
        if "couldn't calculate" in answer or "failed" in answer:
            # Fallback to Gemini for complex word problems or logic
            return geminai(query)
        speak(answer)
        return answer

    # 4. --- General Info & Trivia ---
    if any(word in q for word in ["who is", "what is", "tell me about", "info on", "meaning of"]):
        answer = RealTimeData.get_wiki(q)
        if "not found" in answer or len(answer) < 10:
            # Fallback to Google Search
            search_ans = RealTimeData.google_search(q)
            if "No search results" in search_ans:
                return geminai(query)
            speak(search_ans)
            return search_ans
        speak(answer)
        return answer

    # 6. --- Search Fallback ---
    search_keywords = ["search", "google", "latest", "current", "now", "price", "stock", "where", "location", "weather", "news"]
    if any(word in q for word in search_keywords):
        # Specific sub-cases for weather/news already handled above, but this catches complex phrases
        ask = q
        for word in ["search", "google", "tell me", "what is", "where is"]:
            ask = ask.replace(word, "")
        
        ask = ask.strip()
        if ask == "": ask = q
        
        answer = RealTimeData.google_search(ask)
        if "No search results" in answer or "failed" in answer:
            return geminai(q) # Fallback to AI if search fails
        speak(answer)
        return answer

    # 7. --- AI Global Fallback ---
    return geminai(q)
