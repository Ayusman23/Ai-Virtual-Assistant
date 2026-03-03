import pyttsx3
import speech_recognition as sr
import eel
import time
import threading

# Global engine initialization
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if len(voices) > 1:
        engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 175)
except Exception as e:
    print("TTS Init Error:", e)
    # Fallback to no-engine for non-voice environments
    engine = None

# -------------------------
# STOP SPEAKING FUNCTION
# -------------------------
@eel.expose
def stopSpeaking():
    try:
        engine.stop()
        print("Speech stopped by user.")
        eel.ShowHood()
    except Exception as e:
        print("Error stopping speech:", e)

# ❌ REMOVE all imports from features.py to avoid circular import
# We will import features INSIDE functions instead.


# -------------------------
# TEXT-TO-SPEECH FUNCTION
# -------------------------
def speak(text):
    text = str(text)
    
    eel.DisplayMessage(text)
    eel.receiverText(text)
    
    # Using a thread for speaking makes it easier for the UI to stay responsive, 
    # but pyttsx3 can be finicky with threads. 
    # For now, we'll just call it and rely on engine.stop() from the main thread if possible.
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Speak Error:", e)


# -------------------------
# VOICE LISTENING FUNCTION
# -------------------------
def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("listening....")
        eel.DisplayMessage("listening....")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source, timeout=10, phrase_time_limit=6)

    try:
        print("recognizing....")
        eel.DisplayMessage("recognizing....")

        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)

    except Exception:
        speak("I did not hear you. Please say again.")
        return takecommand()

    return query.lower()


# -----------------------------------------------------
# MAIN COMMAND HANDLER
# -----------------------------------------------------
@eel.expose
def allCommands(message=1):

    # Get query text
    if message == 1:
        query = takecommand()
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)

    try:
        # Import features only when needed (prevents circular import)
        from engine.features import (
            openCommand,
            PlayYoutube,
            findContact,
            whatsApp,
            makeCall,
            sendMessage,
            processQuery
        )

        # Opening apps or websites
        if "open" in query:
            app_name = query.replace("open", "").replace(ASSISTANT_NAME, "").strip()
            speak(f"Sir, do you want me to open {app_name}?")
            response = takecommand()
            if "yes" in response or "ok" in response or "sure" in response or "do it" in response:
                openCommand(query)
            else:
                speak("Operation cancelled.")

        # YouTube search
        elif "on youtube" in query:
            PlayYoutube(query)

        # WhatsApp or Mobile actions
        elif "send message" in query or "phone call" in query or "video call" in query:
            contact_no, name = findContact(query)

            if contact_no != 0:
                speak("Which mode you want to use, WhatsApp or mobile?")
                preference = takecommand()

                if "mobile" in preference:
                    if "send message" in query or "send sms" in query:
                        speak("What message do you want to send?")
                        msg = takecommand()
                        sendMessage(msg, contact_no, name)

                    elif "phone call" in query:
                        makeCall(name, contact_no)

                    else:
                        speak("Please try again")

                elif "whatsapp" in preference:
                    mode = ""
                    if "send message" in query:
                        mode = "message"
                        speak("What message do you want to send?")
                        msg = takecommand()

                    elif "phone call" in query:
                        mode = "call"
                        msg = ""

                    else:
                        mode = "video call"
                        msg = ""

                    whatsApp(contact_no, msg, mode, name)

        # Everything else → AI Chat via Gemini or Real-Time Search
        else:
            processQuery(query)

    except Exception as e:
        print("Auto Error:", e)
        speak("I cannot complete that action.")
