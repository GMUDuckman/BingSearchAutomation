import json
import random
import time
import requests
import sys
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import words_module  # New module for word list and search term logic

# A function to wait for a few seconds, preventing too many requests
def wait_for(sec=2):
    time.sleep(sec)

# PC search

# Get number of words from command line argument, default to 30 if not provided
num_words = 40 # Default value
if len(sys.argv) > 1:
    try:
        num_words = int(sys.argv[1])
        if num_words <= 0:
            print("Number of words must be positive. Using default (30).")
            num_words = 60
    except ValueError:
        print("Invalid number format. Using default (30).")

# Remove direct API call and words_list construction
# words_list = json.loads(response.text)
# print('{0} words selected from {1}'.format(len(words_list), randomlists_url))
words_list = words_module.get_prepared_words(num_words)
print(f'{len(words_list)} search terms prepared.')

# Setup Edge options with stealth settings
options = webdriver.EdgeOptions()
options.add_argument("--window-size=1024,768")
options.add_argument("--log-level=3")  # Suppress most browser logs
options.add_argument("--silent")  # Reduce console output
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# Initialize Edge driver with options and service (avoid network dependency)
try:
    service = Service(executable_path="msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=options)
except Exception as e:
    print(f"WebDriver version or path issue: {e}")
    print("Trying without specifying driver path (system-installed driver)...")
    try:
        driver = webdriver.Edge(options=options)
    except Exception as e2:
        print(f"System WebDriver also failed: {e2}")
        print("Please download Edge WebDriver matching your Edge version from:")
        print("https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
        sys.exit(1)

# Add custom scripts to mask automation indicators
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    // Overwrite the 'navigator.webdriver' property to undefined
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    """
})

wait_for()

driver.get("https://rewards.bing.com")
wait_for(30)

# Perform pc search actions
total_searches = len(words_list)
for num, word in enumerate(words_list):
    # Calculate and display progress
    progress = ((num + 1) / total_searches) * 100
    print(f'[{progress:.1f}%] {num + 1}/{total_searches}. Searching for: {word}')
    
    # word is now a full search phrase
    wait = random.randint(10, 30)
    try:
        driver.get("http://www.bing.com/")
        wait_for(random.uniform(1.5, 4.0))
        search_box = driver.find_element(By.ID, "sb_form_q")
        search_box.clear()
        # Type search phrase (not just word)
        for char in word:
            search_box.send_keys(char)
            time.sleep(random.uniform(0.05, 0.25))
        
        # Occasionally "think" before pressing enter
        if random.random() < 0.3:  # 30% chance to pause longer
            time.sleep(random.uniform(1.0, 2.5))
        else:
            time.sleep(random.uniform(0.3, 1.0))

        search_box.send_keys(Keys.ENTER)

         # Occasionally scroll down on results page
        if random.random() < 0.4:  # 40% chance to scroll
            # Wait before scrolling
            time.sleep(random.uniform(2.0, 5.0))
            # Execute some scrolling
            scroll_amount = random.randint(300, 1000)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
    except Exception as e1:
        logging.error('An error occurred: %s', e1)

    # Check if we need a 15-minute break (every 3 searches)
    if (num + 1) % 3 == 0 and num + 1 < len(words_list):
        print(f"Completed {num + 1} searches. Taking a 15-minute break...")
        wait_for(900)  # 15 minutes = 900 seconds
        print("Break completed. Resuming searches...")
    
    
    wait_between_searches = random.randint(5, 30)  # 5-30 seconds (~1 minute)
    print(f'Waiting {wait_between_searches} seconds before next search...')
    wait_for(wait_between_searches)
    
# Close the browser
driver.quit()
print("Done!")