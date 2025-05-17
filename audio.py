import inspect
import re
from colorama import init, Fore
from pytubefix import YouTube
import os
from pytubefix.cli import on_progress

init()

# ------------------------------------------------------------------------------------------------------

def download_audio(url):
    yt = YouTube(url, on_progress_callback=on_progress)

    audio_stream = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
    yt_title = audio_stream.title

    if "REPLIT_ENVIRONMENT" in os.environ:
        output_path = "./downloads"
    else:

        output_path = os.path.join(os.path.expanduser("~"), "Downloads")
    yt_title = re.sub(r'[<>:"/\\|?*\']', "", yt_title)

    caller = inspect.stack()[1].function

    if caller not in ["download_video_with_user_choice_single"]:
        print(f"\n{Fore.MAGENTA}Downloading {yt_title} as Audio...\n ")
    audio_stream.download(output_path=output_path, filename=f"{yt_title}.mp3")
    if caller not in ["download_video_with_user_choice_single"]:
        print(f"{Fore.CYAN}**** Audio Download Complete ****\n")