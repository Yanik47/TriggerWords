## Trigger Word Monitoring and Notification System

The server (task2) is installed on the computer of the moderator, who needs to receive some data about what users on other computers enter from the keyboard.

The client is launched by double-clicking on quick_start.bat on each monitored computer. I recommend renaming the trig.pyw file to some personalized name for each computer in your area of ​​responsibility. Then you will be able to determine which computer entered the words from the list. You will also receive data about what word he entered and the name of the tab/application where the user entered the data.

The program can have very different purposes, I wrote this code with the idea that in this way it is possible to monitor university students during tests and exams.

## Overview

This project implements a **Trigger Word Monitoring System** that:
1. Tracks specific words entered on the keyboard.
2. Logs detected words along with context (e.g., active window title).
3. Sends notifications to specified Telegram chats via bot integration.

The project consists of two main components:
- **Server (`task2.py`)**: API for managing trigger words, logging, and sending notifications via a Telegram bot.
- **Client (`trig.pyw`)**: A script for monitoring keyboard input, interacting with the server, and sending data.

For simplified deployment, all components are automated through a `.bat` file.

---

## Features

### Server (`task2.py`)
- **API for Trigger Words**:
  - Add, delete, and view trigger words via the Telegram bot.
  - Save the word list to a file (`trigger_words.json`) for persistence.
- **Telegram Notifications**:
  - Send messages with details of detected words to specified chats.

### Client (`trig.pyw`)
- **Keyboard Monitoring**:
  - Tracks text input system-wide.
- **Dynamic Word List Updates**:
  - Periodically fetches the word list from the server.
- **Context Awareness**:
  - Includes the title of the active window where the word was detected.
- **Data Submission**:
  - Sends detected word data to the server's API.

### Automation
- Automatic startup of the server and client via the `quick_start.bat` file.
- Adds both the client (`trig.pyw`) and the server (`task2.py`) to system startup for execution after reboot.

---

## Installation and Launch

### Installation
1. Download and extract the project archive.
2. Double-click the `quick_start.bat` file.

### What happens when you run `quick_start.bat`:
1. **Python check**:
   - Verifies if Python is installed on your computer.
   - If Python is missing, it initiates installation (if configured to do so).
2. **Adding to startup**:
   - Adds `trig.pyw` and `task2.py` to the Windows startup folder for automatic launch after reboot.
3. **Launching processes**:
   - Starts the server (`task2.py`).
   - Starts the client (`trig.pyw`), which begins monitoring keyboard input and communicating with the server.

### After Reboot
- Both processes (`task2.py` and `trig.pyw`) will automatically launch through the system startup folder.

---

## Usage

### Telegram Bot
1. Start the bot using the `/start` command.
2. Use the buttons to manage trigger words:
   - **➕ Add Words**: Add new trigger words.
   - **📋 List Words**: View the current list of trigger words.
   - **✅ Accept**: Finish adding words.

### Keyboard Monitoring
- The program begins monitoring keyboard input immediately upon launch.
- When a trigger word is detected:
  - A notification is sent to the Telegram bot.
  - The word and its context (active window) are logged on the server.

---

## Project Files

- **`task2.py`**: The server for managing trigger words, logging, and sending Telegram notifications.
- **`trig.pyw`**: The client for monitoring keyboard input and interacting with the server.
- **`quick_start.bat`**: Automates installation, adding to startup, and launching the project.
- **`trigger_words.json`**: A file for storing the list of trigger words.

---

## Notes
- This project is designed for Windows.
- To receive notifications, add your Telegram bot token and chat IDs in the `task2.py` file.
- Make sure to run the `quick_start.bat` file as an administrator for proper startup folder configuration.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.
