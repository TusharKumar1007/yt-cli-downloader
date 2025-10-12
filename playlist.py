import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TF INFO/WARN/ERROR logs
os.environ['CUDA_VISIBLE_DEVICES'] = ''   # Suppress GPU logs if not using GPU

from colorama import init, Fore
from audio import download_audio
from batch import download_batch
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager

init()

def download_playlist():
    # Set up Chrome options
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")

    
    option_list = ["Audio", "Video"]
    for i, option in enumerate(option_list, start=1):
        print(f"\t\t{i} --> {option} ")

    # Get user input
    user_input = input("Enter your choice (1 for Audio, 2 for Video): ").strip()
    if user_input not in ["1", "2"]:
        print(f"\t\t{Fore.RED}**** Invalid choice ****\n")
        return

    driver = None
    
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options,
        )
        print("Chrome WebDriver initialized successfully.")
    except Exception as e:
        print(f"{Fore.RED}Chrome WebDriver failed: {e}. Trying Firefox...{Fore.RESET}")

        #assuming chrome browser is not installed or have some error
        #trying with firefox mainly for OS on Linux
        firefox_options = FirefoxOptions()
        firefox_options.add_argument("--headless")

        try:
            driver = webdriver.Firefox(
                service=FirefoxService(GeckoDriverManager().install()),
                options=firefox_options,
            )
            print("Firefox WebDriver initialized successfully.")
        except Exception as e:
            print(f"{Fore.RED}Firefox WebDriver also failed: {e}. Cannot initialize any browser.{Fore.RESET}")
            return

    
    user_link = input("Enter the playlist URL: ").strip()

    try:
        
        driver.get(user_link)

        
        video_link_list = driver.find_elements(By.ID, "video-title")
        link_list = [
            video.get_attribute("href")
            for video in video_link_list
            if video.get_attribute("href")
        ]

        if not link_list:
            print(f"{Fore.YELLOW}No videos found in the playlist.{Fore.RESET}")
            return

        
        if user_input == "1":
            for url in link_list:
                download_audio(url, 'y')  
        elif user_input == "2":
            download_batch(link_list)  

        print(f"{Fore.GREEN}Download complete!{Fore.RESET}")

    except Exception as e:
        print(f"{Fore.RED}An error occurred while processing the playlist: {e}{Fore.RESET}")

    finally:
        if driver:
            driver.quit()
