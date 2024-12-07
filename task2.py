import requests
from flask import Flask, jsonify, request
import telebot
import json
import os
import sys
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__)

# Telegram configuration
TELEGRAM_CHAT_IDS = ['742958385']  # Add necessary Chat IDs here
bot = telebot.TeleBot('7586258518:AAE6STcQzi9Wb0c0hVmcJRCY5PdRuTFrQrE')

# Path to the file for storing the list of words
WORDS_FILE = "trigger_words.json"


# Load the list of words from the file
def load_words():
    if os.path.exists(WORDS_FILE):
        with open(WORDS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []


# Save the list of words to the file
def save_words(words):
    with open(WORDS_FILE, 'w', encoding='utf-8') as file:
        print("Saving updated word list to file...")
        json.dump(words, file, ensure_ascii=False, indent=4)


# Initialize the list of trigger words
word_lists = load_words()
user_name = ""

# Dictionary for tracking add word mode for each chat 
add_mode = {}

# Function to create the main keyboard
def main_menu_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        KeyboardButton("➕ Add Words"),
        KeyboardButton("✅ Accept"),
        KeyboardButton("📋 List Words")
    )
    return markup

@app.route('/api/log_trigger', methods=['POST'])
def log_trigger_word():
    data = request.get_json()
    word = data.get("word")
    user_name = data.get("user")
    context = data.get("context")

    if word and user_name:
        message = f"Triggered word: '{word}'\nUser: {user_name}\nContext: {context}"
        print(message.encode('utf-8').decode('utf-8'))
        send_to_telegram(message)
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"error": "Missing word or user data"}), 400

# Route to get the list of trigger words hello 
@app.route('/api/trigger_words', methods=['GET'])
def get_trigger_words():
    return jsonify({"words": word_lists})

# Start command to show the main menu
@bot.message_handler(commands=['start'])
def start_bot(message):
    if str(message.chat.id) in TELEGRAM_CHAT_IDS:
        bot.send_message(
            message.chat.id,
            "Welcome! Use the buttons below to interact with the bot.",
            reply_markup=main_menu_keyboard()
        )



# Handle the Add Words button
@bot.message_handler(func=lambda message: message.text == "➕ Add Words")
def enable_add_mode(message):
    if str(message.chat.id) in TELEGRAM_CHAT_IDS:
        chat_id = message.chat.id
        add_mode[chat_id] = True
        bot.send_message(chat_id, "Add word mode enabled. Send the words you want to add.")


# Handle the Accept button
@bot.message_handler(func=lambda message: message.text == "✅ Accept")
def disable_add_mode(message):
    if str(message.chat.id) in TELEGRAM_CHAT_IDS:
        chat_id = message.chat.id
        add_mode[chat_id] = False
        bot.send_message(chat_id, "Add word mode disabled. Words will no longer be accepted.")


# Handle the List Words button
@bot.message_handler(func=lambda message: message.text == "📋 List Words")
def list_words(message):
    if str(message.chat.id) in TELEGRAM_CHAT_IDS:
        if word_lists:
            words_str = ', '.join(word_lists)
            bot.send_message(message.chat.id, f"Word list: {words_str}")
        else:
            bot.send_message(message.chat.id, "The word list is empty.")


# Handle user text input
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if add_mode.get(chat_id, False):
        words = message.text.split()
        new_words = []
        if str(chat_id) in TELEGRAM_CHAT_IDS:
            for word in words:
                # Add the word if it is not already in word_lists
                if word not in word_lists and word[0] != '/':
                    word_lists.append(word)
                    new_words.append(word)
            # Save the updated list to the file  
            if new_words:
                save_words(word_lists)
                bot.send_message(chat_id, f"Words added to the list: {', '.join(new_words)}")
            else:
                bot.send_message(chat_id, "All words are already in the list.")
        print("Updated word list:", word_lists)
    else:
        bot.send_message(chat_id, "Please use the buttons to select an action.", reply_markup=main_menu_keyboard())


# Function to send a message to multiple Telegram chats
def send_to_telegram(message):
    for chat_id in TELEGRAM_CHAT_IDS:
        try:
            bot.send_message(chat_id, message)
            print(f"Message sent to chat {chat_id}: {message}")
        except Exception as e:
            print(f"Error sending message to chat {chat_id}: {e}")


if __name__ == '__main__':
    # Start the Flask server in a separate thread so it doesn't block the Telegram bot
    from threading import Thread

    Thread(target=lambda: app.run(debug=True, use_reloader=False)).start()

    # Start the Telegram bot
    bot.polling(none_stop=True)
