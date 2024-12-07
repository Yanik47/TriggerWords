import os
import requests
from pynput.keyboard import Listener, Key
import threading
import time
import platform
import win32gui  

script_name = os.path.basename(__file__)
print(f"Current file name: {script_name}")

# API URL to get the list of trigger words
API_URL = "http://localhost:5000/api/trigger_words?server=server1"
LOG_URL = "http://localhost:5000/api/log_trigger"

# Global variable to store the list of trigger words
trigger_words = []

# Function to fetch the list of trigger words from API
def fetch_trigger_words():
    global trigger_words
    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        trigger_words = data.get("words", [])
        print("Trigger word list updated:", trigger_words)
    except requests.RequestException as e:
        print(f"Error accessing API: {e}")

# Function to get the current active window title
def get_active_window_title():
    if platform.system() == "Windows":
        try:
            window = win32gui.GetForegroundWindow()
            return win32gui.GetWindowText(window)
        except Exception as e:
            print(f"Error getting active window title: {e}")
            return "Unknown Window"
    else:
        return "Non-Windows platform"

# Function to send the triggered word and its context to the server
def send_trigger_word(word, context):
    try:
        payload = {
            "word": word,
            "user": script_name,
            "context": context
        }
        response = requests.post(LOG_URL, json=payload)
        response.raise_for_status()
        print(f"Triggered word '{word}' sent to server successfully with context: {context}")
    except requests.RequestException as e:
        print(f"Error sending triggered word to server: {e}")

# Background function to periodically update the trigger word list
def update_trigger_words_periodically():
    while True:
        fetch_trigger_words()
        time.sleep(30)  # Wait for 30 seconds before next update

# Initialize the list of trigger words
fetch_trigger_words()
current_word = ""

def on_press(key):
    global current_word
    try:
        current_word += key.char
    except AttributeError:
        # If a special character (not a letter) is pressed, reset the current string
        if key == Key.space or key == Key.enter:
            current_word = ""
        return

    # Check if the entered word matches one of the words in the list
    for word in trigger_words:
        if word.lower() in current_word.lower():
            context = get_active_window_title()  # Get active window title as context
            send_trigger_word(word, context)
            current_word = ""  # Reset the word after triggering
            break

def on_release(key):
    # Stop the program on ESC key press
    pass

# Start a background thread to update the word list every hour
threading.Thread(target=update_trigger_words_periodically, daemon=True).start()

# Start the global keyboard listener
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
