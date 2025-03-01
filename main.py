from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time, requests, json, os, re, multiprocessing

def extract_string_from_brackets(s):
    match = re.search(r'\[(\w+)\]', s)
    if match:
        return match.group(1)
    else:
        return None

def video_download(url, session, episode, title, download_folder_path):
    print(f"Start for {title}_{episode}")
    response = session.get(url)
    if (response.status_code == 200):
        file_name = os.path.join(download_folder_path,f'{title}_{episode}.mp4')
        with open(f'{file_name}', 'wb') as f:
            f.write(response.content)
        print(f'Video {title}_{episode} saved in {file_name}.')
    else:
        print(f"Video {title}_{episode} downloaded failed: {response.status_code}")


config_path = "./config.json"

with open(config_path, 'r') as file:
    data = json.load(file)

download_folder_main_path = data["download_path"]
wait_time = data["web_wait_time"]

# Set up Edge options to run in headless mode
edge_options = Options()
edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--mute-audio")

driver = webdriver.Edge(options=edge_options)

def main():
    try:
        while True:
            # Open the webpage
            url = input("Web url ('exit' to quit): ")
            if url.lower() in ["exit", "quit"]:
                break

            # Initialize the WebDriver with the headless option
            print(f"Access {url}")
            driver.get(url)

            # Give the page some time to load
            time.sleep(wait_time)

            # Get title
            element = driver.find_element(By.CSS_SELECTOR, 'span.cat-links > a')
            title = element.text
            print(f"Title: {title}")

            download_folder_path = os.path.join(download_folder_main_path,title)
            os.makedirs(download_folder_path, exist_ok=True)
            print(f"Target folder: {download_folder_path}")

            # Find all <article> elements
            articles = driver.find_elements(By.TAG_NAME, 'article')

            # Get the number of video
            n_video = len(articles)
            print(f"{n_video} ready to download.")

            processes = []

            # Loop through each <article> and interact with the <video>
            for i in range(n_video):
                try:
                    # Get the access cookies
                    if (driver.current_url != url):
                        print(f"Access {url}")
                        driver.get(url)
                        time.sleep(wait_time)
                    articles = driver.find_elements(By.TAG_NAME, 'article')
                    article = articles[i]
                    header_h2_a = article.find_elements(By.CSS_SELECTOR, 'header > h2 > a')
                    header_h2 = article.find_elements(By.CSS_SELECTOR, 'header > h2')
                    if header_h2_a:
                        episode_tmp = header_h2_a[0].text
                        episode = extract_string_from_brackets(episode_tmp)
                    elif header_h2:
                        episode_tmp = header_h2[0].text
                        episode = extract_string_from_brackets(episode_tmp)
                    else:
                        episode = f"{(n_video - i):02}"
                    video_button = article.find_element(By.TAG_NAME, 'button')
                    video_button.click()
                    
                    # Get /.mp4 url (example: https://miru.v.anime1.me/1590/4b.mp4)
                    video_src = ""
                    while video_src == "":
                        time.sleep(0.5)
                        video = article.find_element(By.TAG_NAME, 'video')     
                        video_src = video.get_attribute('src')
                    
                    # Open video src
                    driver.get(video_src)
                    time.sleep(wait_time)

                    cookies = driver.get_cookies()
                    session = requests.Session()
                    for cookie in cookies:
                        session.cookies.set(cookie['name'], cookie['value'])
                    
                    p = multiprocessing.Process(target=video_download, args=(video_src, session, episode, title, download_folder_path))
                    p.start()
                    processes.append(p)

                except Exception as e:
                    print(f"An error occurred: {e}")
                
            for process in processes:
                process.join()

            time.sleep(wait_time)
    finally:
        # Close the WebDriver
        driver.quit()

if __name__ == '__main__':
    main()