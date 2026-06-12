import json
import time
import logging
import random
import requests
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import words_module  # New module for word list and search term logic

# A function to wait for a few seconds, preventing too many requests
def wait_for(sec=2):
    time.sleep(sec)

# Mobile search

# Get number of words from command line argument, default to 20 if not provided
num_words = 30  # Default for mobile
if len(sys.argv) > 1:
    try:
        num_words = int(sys.argv[1])
        if num_words <= 0:
            print("Number of words must be positive. Using default (20).")
            num_words = 20
    except ValueError:
        print("Invalid number format. Using default (20).")

# Get random words from API
# randomlists_url = f"https://random-word-api.herokuapp.com/word?number={num_words}"
# response = requests.get(randomlists_url)
# words_list = json.loads(response.text)
# print('{0} words selected from {1}'.format(len(words_list), randomlists_url))
words_list = words_module.get_prepared_words(num_words)
print(f'{len(words_list)} search terms prepared.')

# Define mobile emulation with a randomly selected mobile user agent
mobile_user_agents = [
    "Mozilla/5.0 (Android 14; Mobile; rv:136.0) Gecko/136.0 Firefox/136.",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.3"
]

# Pick a random user agent
selected_user_agent = random.choice(mobile_user_agents)

# Configure mobile emulation settings
mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": selected_user_agent
}

# Set up Edge options with mobile emulation and anti-detection features
edge_options = webdriver.EdgeOptions()
edge_options.add_argument("--log-level=3")  # Suppress most browser logs
edge_options.add_argument("--silent")  # Reduce console output
edge_options.add_experimental_option("mobileEmulation", mobile_emulation)
edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
edge_options.add_experimental_option('useAutomationExtension', False)

# Create Edge WebDriver instance with options
try:
    service = Service(executable_path="msedgedriver.exe")
    driver = webdriver.Edge(service=service, options=edge_options)
except Exception as e:
    print(f"WebDriver version mismatch error: {e}")
    print("Trying without specifying driver path...")
    try:
        # Let Selenium find the system-installed WebDriver
        driver = webdriver.Edge(options=edge_options)
    except Exception as e2:
        print(f"System WebDriver also failed: {e2}")
        print("Please download Edge WebDriver version 140 from:")
        print("https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/")
        sys.exit(1)

# Set window size with slight randomization to appear more natural
window_width = random.randint(350, 390)
window_height = random.randint(620, 680)
driver.set_window_size(window_width, window_height)

# Add custom script to hide automation indicators
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    // Hide webdriver property
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    });
    """
})

# Load Bing rewards page
driver.get("https://rewards.bing.com")
# Wait a randomized time on first page load
initial_wait = random.randint(8, 15)
wait_for(initial_wait)

# Perform mobile search actions
total_searches = len(words_list)
for num, word in enumerate(words_list):
    # Calculate and display progress
    progress = ((num + 1) / total_searches) * 100
    print(f'[{progress:.1f}%] {num + 1}/{total_searches}. Searching for: {word}')
    
    # word is now a full search phrase
    wait = random.randint(10, 30)
    try:
        # Navigate to Bing
        driver.get("http://www.bing.com/")
        # Random wait before starting to type
        wait_for(random.uniform(1.5, 4.0))
        
        # Find search box
        search_box = driver.find_element(By.ID, "sb_form_q")
        search_box.clear()
        
        # Type search phrase (not just word)
        for char in word:
            search_box.send_keys(char)
            # Mobile typing is usually a bit slower than desktop
            time.sleep(random.uniform(0.08, 0.35))
        
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
    
    
    wait_between_searches = random.randint(5, 45)  # 5-45 seconds
    print(f'Waiting {wait_between_searches} seconds before next search...')
    wait_for(wait_between_searches)

# Close the browser
driver.quit()
print("Done!")