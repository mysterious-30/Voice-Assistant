import re
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Assigning Variables
CHROME_PROFILE_PATH = "user-data-dir=D:/Jarvis24/Data/profile"
CONTACTS_FILE_PATH = "D:/Jarvis/Data/contacts.json"

# Configure Chrome WebDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(CHROME_PROFILE_PATH)
chrome_options.add_argument("--headless")  # Remove for debugging
chrome_options.add_argument("--disable-gpu")

# Function to send a WhatsApp message
def Whatsapp_msg(query):
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
    contact_number = contacts.get(contact_name)
    if not contact_number:
        print(f"Error: Contact '{contact_name}' not found in the contacts file.")
        return

    # Initialize WebDriver and navigate to WhatsApp Web
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.whatsapp.com/")
    print("Using stored profile to access WhatsApp Web...")

    try:
        # Wait for the search box to appear
        search_box = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
        )
        print("Search box located. Searching for contact:", contact_number)

        # Search for the contact
        search_box.click()
        search_box.clear()
        search_box.send_keys(contact_number)
        sleep(2)  # Allow search results to load
        search_box.send_keys(Keys.RETURN)  # Open the chat

        # Wait for the message input box
        message_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
        )
        print("Message box located. Sending message to:", contact_number)

        # Type and send the message
        message_box.send_keys(message_content)
        message_box.send_keys(Keys.RETURN)  # Send the message
        sleep(5)
        print(f"Message '{message_content}' sent successfully to {contact_name} ({contact_number})!")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()

# Example usage
if __name__ == "__main__":
    test_query = "Akash : Hello, this is a test message!"
    Whatsapp_msg(test_query)
