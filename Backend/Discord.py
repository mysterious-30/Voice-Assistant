import tls_client
import datetime
import time
import re
import json

# Assigning Variables
TOKEN = "NDk3OTkwOTkyMjk3NzIxODY4.G5Egrp.CLWwhmtwRxwoR3i0kUCRXYen1ZrWMLL44RVEls"
SERVER_ID = "@me"
DISCORD_API_URL = "https://discord.com/api/v9/channels/{channel_id}/messages"
CONTACTS_FILE_PATH = "D:/Jarvis/Data/discord.json"

# Initialize TLS session
session = tls_client.Session(client_identifier='chrome_120', random_tls_extension_order=True)

# Generate a unique nonce for Discord messages
def generate_nonce():
    current_time = datetime.datetime.now()
    unix_timestamp = time.mktime(current_time.timetuple())
    return str((int(unix_timestamp) * 1000 - 1420070400000) * 4194304)

# Create headers for the Discord API request
def create_headers(token, server_id, channel_id):
    return {
        'authority': 'discord.com',
        'accept': '*/*',
        'authorization': token,
        'content-type': 'application/json',
        'origin': 'https://discord.com',
        'referer': f'https://discord.com/channels/{server_id}/{channel_id}',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'x-discord-locale': 'en-GB',
        'x-discord-timezone': 'Asia/Calcutta',
    }

# Create a payload for the Discord message
def create_payload(content):
    return {
        'mobile_network_type': 'unknown',
        'content': content,
        'nonce': generate_nonce(),
        'tts': False,
        'flags': 0,
    }

# Send a message via Discord API
def send_message(token, server_id, channel_id, content):
    url = DISCORD_API_URL.format(channel_id=channel_id)
    headers = create_headers(token, server_id, channel_id)
    payload = create_payload(content)

    try:
        response = session.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}, Error: {response.text}")
    except Exception as e:
        print(f"An error occurred while sending the message: {e}")

# Main function to process and send a Discord message
def Discord_msg(query):
    # Validate query format
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
    channel_id = contacts.get(contact_name)
    if not channel_id:
        print(f"Error: Contact '{contact_name}' not found in the contacts file.")
        return

    # Send the message
    send_message(TOKEN, SERVER_ID, channel_id, message_content)

# Example usage
if __name__ == "__main__":
    test_query = "ken : Hello, how are you? ,  This Is an automated message"
    Discord_msg(test_query)
