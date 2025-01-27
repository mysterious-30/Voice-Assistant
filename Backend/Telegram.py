from telethon import TelegramClient
import json
import re
import time
import datetime
import asyncio

# Assigning Variables
API_ID = 23915082
API_HASH = 'a00045e3df8dd8b92f2699b6d6a14157'
PHONE_NUMBER = '+916306476385'  # Your phone number with country code
CONTACTS_FILE_PATH = "D:/Jarvis/Data/telegram.json"  # Path to your contacts file

# Initialize the Telegram client
client = TelegramClient('telegram_bot_session', API_ID, API_HASH)

# Generate a unique timestamp for the message (to simulate a nonce)
def generate_nonce():
    current_time = datetime.datetime.now()
    unix_timestamp = time.mktime(current_time.timetuple())
    return str(int(unix_timestamp))

# Send a message via Telegram API (async version)
async def send_message(user_id, content):
    try:
        await client.send_message(user_id, content)
        print("Message sent successfully!")
    except Exception as e:
        print(f"An error occurred while sending the message: {e}")

# Main function to process and send a Telegram message
async def telegram_msg(query):
    # Validate query format (e.g., "John : Hello, how are you?")
    match = re.match(r"([a-zA-Z\s]+) : (.+)", query)
    if not match:
        print("Invalid query format. Use '[Contact Name] : [Message]'.")
        return

    # Extract contact name and message content
    contact_name = match.group(1).strip()
    message_content = match.group(2).strip()

    # Load contacts from JSON file
    try:
        with open(CONTACTS_FILE_PATH, "r") as file:
            contacts = json.load(file)
        print("Contacts loaded successfully.")
    except FileNotFoundError:
        print(f"Error: The contacts file '{CONTACTS_FILE_PATH}' was not found.")
        return
    except json.JSONDecodeError:
        print("Error: Failed to decode the contacts file. Ensure it contains valid JSON.")
        return

    # Lookup contact by name
    user_id = contacts.get(contact_name)
    if not user_id:
        print(f"Error: Contact '{contact_name}' not found in the contacts file.")
        return

    # Send the message
    await send_message(user_id, message_content)

# Main entry point to run the client
async def main():
    await client.start(PHONE_NUMBER)  # Start the client with the phone number
    test_query = "Akash : If You Have Received this message then the admin has successfully configured the bot"
    await telegram_msg(test_query)

# Run the client
if __name__ == "__main__":
    asyncio.run(main())
