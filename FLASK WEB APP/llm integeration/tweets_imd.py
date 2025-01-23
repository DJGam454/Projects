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

# Initialize the Chrome WebDriver in headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(ChromeDriverManager(driver_version="131.0.6778.204").install()), options=chrome_options)

def scroll_and_collect(url, num_items, item_selector):
    driver.get(url)
    items = []
    scroll_attempts = 0  # To prevent infinite scrolling

    while len(items) < num_items and scroll_attempts < 10:
        try:
            # Wait for the tweet elements to load
            WebDriverWait(driver, 40).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, item_selector))
            )
            
            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            item_divs = soup.select(item_selector)
            
            # Collect tweet text, time, and images
            for item_div in item_divs:
                if len(items) >= num_items:
                    break
                item_text = item_div.find('div', {'lang': True})
                item_time = item_div.find('time')
                
                # Look for images within the tweet article
                image_urls = []
                image_elements = item_div.find_all('img')
                for img in image_elements:
                    image_url = img['src']
                    # Filter out profile pictures or irrelevant images
                    if 'profile_images' not in image_url:
                        image_urls.append(image_url)
                
                if item_text and item_time:
                    item_data = {
                        "Tweet": item_text.text.strip(),
                        "Time": item_time['datetime'],
                        "Images": image_urls if image_urls else []  # Use an empty list instead of None
                    }
                    items.append(item_data)
            
            # Scroll down to load more tweets
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

            scroll_attempts += 1  # Increment scroll attempts to avoid infinite scroll

        except Exception as e:
            print(f"An error occurred while scrolling and collecting: {str(e)}")
            break

    if not items:
        print("No items were collected. The page structure might have changed.")
    return items

def fetch_tweets(username, num_tweets=10):
    url = f"https://x.com/{username}"
    item_selector = "article[role='article']"  # Selector to target tweet articles
    return scroll_and_collect(url, num_tweets, item_selector)

# Function to save tweets to a CSV file
def save_tweets_to_csv(tweets, filename="fetched_tweets.csv"):
    keys = tweets[0].keys()  # Get the keys from the first tweet to use as column headers
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for tweet in tweets:
            # Join image URLs into a single string
            tweet['Images'] = ', '.join(tweet['Images']) if tweet['Images'] else ""
            writer.writerow(tweet)
    print(f"Tweets saved to {filename}")

# Example usage
username = "Indiametdept"  # Replace with the desired Twitter username
tweets = fetch_tweets(username, 10)

# Save the fetched tweets and images to a CSV file
if tweets:
    save_tweets_to_csv(tweets, "B:\\OneDrive - Amity University\\Desktop\\CSVs\\fetched_tweets_IMD.csv")

# Print the fetched tweets with images
for idx, tweet in enumerate(tweets, start=1):
    print(f"Tweet {idx}: {tweet['Tweet']} (Time: {tweet['Time']})")
    if tweet['Images']:
        print(f"Images: {tweet['Images']}")
    else:
        print("No images in this tweet.")

driver.quit()
