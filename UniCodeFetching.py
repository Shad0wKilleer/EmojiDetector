from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize WebDriver (Make sure you have the correct WebDriver installed)
driver = webdriver.Chrome()

# Open WhatsApp Web
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 20)

# Wait for QR code scan
input("📌 Scan the QR Code and press ENTER...")

# Search for a contact and open chat
contact_name = "Me (You)"
search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']")))
search_box.click()
search_box.send_keys(contact_name)
time.sleep(2)
search_box.send_keys(Keys.ENTER)

# Open Emoji Panel
emoji_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Emoji']")))
emoji_button.click()
time.sleep(2)

# Get the emoji elements
emojis = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//span[contains(@data-emoji, '')]")))

# Iterate through emojis
for emoji in emojis:
    try:
        # Click the emoji
        emoji.click()
        time.sleep(0.5)  # Allow time for the emoji to appear in the input box

        # Check if a variant selector appears
        try:
            variant = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'variant-selector')]//span")))
            variant.click()
        except:
            pass  # No variant selector means the emoji was added directly

    except Exception as e:
        print(f"❌ Error sending emoji: {e}")
        continue

# Locate the input box and send the message
input_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true']")))
input_box.send_keys(Keys.ENTER)

print("✅ Emojis sent successfully!")

# Close browser after sending
time.sleep(3)
driver.quit()