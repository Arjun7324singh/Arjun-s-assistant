import pyttsx3
import speech_recognition as sr
import os
import datetime
import time
import screen_brightness_control as sbc
import cv2
import pyautogui
import webbrowser
import smtplib
from email.message import EmailMessage
import keyboard # 🔹 Import the keyboard library

# 🔹 Global state to toggle between voice and text modes
voice_mode_active = True

# 🔹 Speak/Print function based on mode
def speak_or_print(text):
    if voice_mode_active:
        engine.say(text)
        print("Assistant:", text)
        engine.runAndWait()
        time.sleep(0.3)
    else:
        print("Assistant:", text)

# 🔹 Initialize Text-to-Speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

# 🔹 Function to wish the user based on the time of day
def wishme():
    '''This function wishes the user based on the time of day.'''
    hour = int(datetime.datetime.now().hour)
    
    if 0 <= hour < 12:
        speak_or_print("Good Morning sir, Have a nice day ahead")
    elif 12 <= hour < 18:
        speak_or_print('Good Afternoon sir')
    elif 18 <= hour <= 21:
        speak_or_print('Good Evening Sir')
    else:
        speak_or_print("Good Night Sir")
    
    speak_or_print('I am Jessica, Please tell me how may I help you?')

# 🔹 Speech/Text to text function
def take_command():
    if not voice_mode_active:
        return input("Type your command: ").lower()

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=7)
        except Exception:
            return "None"
        
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    
    except Exception:
        print("Sorry, I did not understand that. Please try again.")
        return "None"
    return query

# 🔹 Function to toggle the mode
def toggle_mode():
    global voice_mode_active
    voice_mode_active = not voice_mode_active
    if voice_mode_active:
        speak_or_print("Voice mode activated.")
    else:
        speak_or_print("Text mode activated.")

# 🔹 Placeholder for a free AI service
def ask_ai(prompt):
    speak_or_print("Sorry, I cannot access an AI service right now. Please use a regular command.")

# 🔹 Computer control functions
def set_brightness(level):
    try:
        sbc.set_brightness(level)
        speak_or_print(f"Setting brightness to {level} percent.")
    except Exception:
        speak_or_print("Sorry, I couldn't change the screen brightness.")

# 🔹 Camera functionality
def open_camera():
    speak_or_print("Opening camera. Press 'q' on the keyboard to close.")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak_or_print("Error: Could not access the camera.")
        return
    
    while True:
        ret, frame = cap.read()
        cv2.imshow('Camera Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


# 🔹 Screenshot functionality
def take_screenshot():
    try:
        speak_or_print("Taking a screenshot.")
        screenshot = pyautogui.screenshot()
        file_path = "screenshot.png"
        screenshot.save(file_path)
        speak_or_print("Screenshot saved as screenshot.png.")
    except Exception as e:
        speak_or_print("Sorry, I couldn't take a screenshot.")
        print(e)

# 🔹 Email functionality
def send_email(to_email, subject, body):
    # Your email credentials - Use environment variables for security!
    sender_email = os.environ.get("arjun7324singh@gmail.com")
    password = os.environ.get("@#arjun123")

    # Create the email message
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        # Connect to the SMTP server (for Gmail, it's smtp.gmail.com)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, password)
            server.send_message(msg)
        speak_or_print("Email sent successfully.")
        print("Email sent!")
    except Exception as e:
        speak_or_print("Sorry, I was unable to send the email.")
        print(f"Error sending email: {e}")

# 🔹 Open web browser and search functionality
def open_browser():
    speak_or_print("Opening your default web browser. What would you like to search?")
    search_query = take_command()
    if search_query != "none":
        url = f"https://www.google.com/search?q={search_query}"
        webbrowser.open(url)
        speak_or_print(f"Searching for {search_query} on Google.")
    else:
        speak_or_print("Sorry, I couldn't hear the search query.")

if __name__ == "__main__":
    # 🔹 Add the hotkey listener from the keyboard library
    keyboard.add_hotkey('ctrl+t', toggle_mode)

    wishme() # Calls the wishme function when the script starts

    while True:
        command = take_command().lower()

        if "quit" in command or "exit" in command:
            speak_or_print("Goodbye! Have a great day!")
            break

        elif "open notepad" in command:
            speak_or_print("Opening Notepad now.")
            os.system("start notepad")
        
        elif "open calculator" in command:
            speak_or_print("Opening Calculator now.")
            os.system("start calc")
        
        elif "open settings" in command:
            speak_or_print("Opening Settings now.")
            os.system("start ms-settings:")
            
        elif "open browser" in command:
            open_browser()

        elif "set brightness to" in command:
            try:
                brightness_level = int(''.join(filter(str.isdigit, command)))
                if 0 <= brightness_level <= 100:
                    set_brightness(brightness_level)
                else:
                    speak_or_print("Please provide a value between 0 and 100.")
            except ValueError:
                speak_or_print("I couldn't understand the brightness level. Please say a number.")

        elif "open camera" in command:
            open_camera()

        elif "take screenshot" in command:
            take_screenshot()

        elif "ask ai" in command:
            speak_or_print("AI mode activated. What's your question?")
            ai_query = take_command()
            if ai_query != "none":
                ask_ai(ai_query)

        elif "what can you do" in command or "help" in command:
            speak_or_print("I can open Notepad, Calculator, Settings, a web browser, change brightness, open the camera, and take screenshots.")
        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%H:%M")
            speak_or_print(f"The current time is {current_time}.")

        elif "send email" in command:
            speak_or_print("Please tell me the receiver's email address.")
            to = take_command()
            
            if to != "none":
                speak_or_print("What should be the subject?")
                subject = take_command()
                
                if subject != "none":
                    speak_or_print("What message should I send?")
                    message = take_command()
                    
                    if message != "none":
                        send_email(to, subject, message)
                    else:
                        speak_or_print("I could not get the message. Aborting email sending.")
                else:
                    speak_or_print("I could not get the subject. Aborting email sending.")
            else:
                speak_or_print("I could not get the recipient. Aborting email sending.")
        
        else:
            speak_or_print("I didn't understand that command. Please try again.")