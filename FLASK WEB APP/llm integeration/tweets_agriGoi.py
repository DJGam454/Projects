import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager  # Use WebDriverManager to manage ChromeDriver

# Initialize the Chrome WebDriver without headless mode for debugging
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="131.0.6778.204").install()), options=chrome_options)

def scroll_and_collect(url, num_items, item_selector):
    driver.get(url)
    items = []
    scroll_attempts = 0

    while len(items) < num_items and scroll_attempts < 10:
        try:
            
            WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, item_selector))
            )
            
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            item_divs = soup.select(item_selector)
            
            
            for item_div in item_divs:
                if len(items) >= num_items:
                    break
                
                
                item_text = item_div.find('div', {'lang': True})
                
                
                image_element = item_div.find('img', {'src': True})  
                image_link = image_element['src'] if image_element else None
                
                
                item_time = item_div.find('time')
                
                if item_text and item_time:
                   
                    combined_data = f"Tweet: {item_text.text.strip()}\nImage Link: {image_link if image_link else 'No Image'}\nTime: {item_time['datetime']}\n"
                    items.append(combined_data)  # Store the combined string
                    
          
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  

            scroll_attempts += 1  

        except Exception as e:
            print(f"An error occurred while scrolling and collecting: {str(e)}")
            break

    if not items:
        print("No items were collected. The page structure might have changed.")
    return items

def fetch_tweets(username, num_tweets=10):
    url = f"https://x.com/{username}"
    item_selector = "article[role='article']"  
    return scroll_and_collect(url, num_tweets, item_selector)

# Example usage
username = "AgriGoI"  
tweets_Agri= fetch_tweets(username, 10)

driver.quit()

