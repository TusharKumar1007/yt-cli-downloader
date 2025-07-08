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
from selenium.webdriver.chrome.options import Options
init()
# ------------------------------------------------------------------------------------------------------

def download_playlist():
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # Useful for headless mode

    # Option selection
    option_list = ["Audio", "Video"]
    for i, option in enumerate(option_list, start=1):
        print(f"\t\t{i} --> {option} ")

    # Get user input
    user_input = input("Enter your choice (1 for Audio, 2 for Video): ").strip()
    if user_input not in ["1", "2"]:
        print(f"\t\t{Fore.RED}**** Invalid choice ****\n")
        return

    # Initialize Chrome WebDriver
    try:
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options,
        )
    except Exception as e:
        print(f"{Fore.RED}Error initializing the Chrome WebDriver: {e}{Fore.RESET}")
        return

    # Get URL input
    user_link = input("Enter the playlist URL: ").strip()

    try:
        # Access the playlist page
        driver.get(user_link)

        # Find all video links
        video_link_list = driver.find_elements(By.ID, "video-title")
        link_list = [
            video.get_attribute("href")
            for video in video_link_list
            if video.get_attribute("href")
        ]

        if not link_list:
            print(f"{Fore.YELLOW}No videos found in the playlist.{Fore.RESET}")
            return

        # Process links based on user choice
        if user_input == "1":
            for url in link_list:
                download_audio(url,'y')  # Ensure download_audio is defined
        elif user_input == "2":
            download_batch(link_list)  # Ensure download_batch is defined

        print(f"{Fore.GREEN}Download complete!{Fore.RESET}")

    except Exception as e:

        pass

        # print(
        #     f"{Fore.RED}An error occurred while processing the playlist: {e}{Fore.RESET}"
        # )

    finally:
        # Quit the WebDriver
        driver.quit()
