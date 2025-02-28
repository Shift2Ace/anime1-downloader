from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
import time
import requests

# Set up Edge options to run in headless mode
edge_options = Options()
edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--no-sandbox")

# Initialize the WebDriver with the headless option
driver = webdriver.Edge(options=edge_options)

# Open the webpage
url = 'https://anime1.me/24985'
driver.get(url)

# Give the page some time to load
time.sleep(5)

# Find all <article> elements
articles = driver.find_elements(By.TAG_NAME, 'article')

# Loop through each <article> and interact with the <video>
for article in articles:
    try:
        # Find the <video> element within the <article>
        video_button = article.find_element(By.TAG_NAME, 'button')
        
        # Click the video to play it
        video_button.click()
        
        # Give the video some time to load
        time.sleep(1)

        video = article.find_element(By.TAG_NAME, 'video')     
        video_src = video.get_attribute('src')
        print(f'The video source URL is: {video_src}')

        # Use the same browser session to download the video
        cookies = driver.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Referer': url,
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        response = session.get(video_src, headers=headers, stream=True)
        if response.status_code == 200:
            with open('downloaded_video.mp4', 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            print("Video downloaded successfully and saved as 'downloaded_video.mp4'")
        else:
            print(f"Failed to download the video. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Close the WebDriver
driver.quit()