import os
from colorama import init, Fore
from pytubefix import YouTube

from pytubefix.cli import on_progress
from http.client import IncompleteRead
from downloader import (
    download_video_with_user_choice_single,
    download_video_with_user_choice_single_fast,
)
from config import retry_count

init()

# ------------------------------------------------------------------------------------------------------


def download_video_with_user_choice_batch(video_url, output_path, default_res):

    try:
        title = download_video_with_user_choice_single_fast(video_url, default_res)
        return title

    except IncompleteRead:
        retry_count += 1
        if retry_count <= 2:
            print(
                f"\n\t\t{Fore.RED}**** Incomplete Donwload. Retrying download... ****"
            )
            return download_video_with_user_choice_single_fast(
                video_url, output_path, default_res
            )
        else:
            return print(
                f"\n\t\t{Fore.RED}Try downloading {title} Url:{video_url} using option 1..."
            )
    except KeyboardInterrupt:
        print(f"\n\t\t{Fore.RED}**** Aborting ****")
    except Exception as e:
        print(f"Error: {e}")
        pass


# ------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------------------------------


def fetch_links_from_text_file():
    links = []
    with open("ytlinks.txt", "r+") as f:
        for line in f.readlines():
            links.append(line.rstrip())
    return links


# ------------------------------------------------------------------------------------------------------


def download_batch(yt_link_list, default_res="720p"):
    if len(yt_link_list) == 0:
        raise Exception
    resolution = input(
        f"Enter resolution 360, 480, 720 or 1080 press enter to download in {default_res}:  "
    ).strip()

    if resolution in ["360", "480", "720", "1080"]:
        default_res = resolution + "p"

    print(
        f"\n\t\t{Fore.CYAN}**** Number of Videos at {default_res} to be Downloaded: {len(yt_link_list)} ****"
    )
    for index, link in enumerate(yt_link_list):
        video_url = f"{link}"
        print(f"{Fore.CYAN}Downloading {index+1}/{len(yt_link_list)}")
        output_path = os.path.join(os.path.expanduser("~"), "Downloads\\")

        if default_res in ["480p", "1080p", "720p"]:
            title, psudo_error_code = download_video_with_user_choice_single(
                link, default_res
            )
            # print(psudo_error_code)
            if psudo_error_code == 404:
                print(f"\n{Fore.YELLOW}Trying to download in 720p\n")
                download_video_with_user_choice_batch(video_url, output_path, "720p")
        else:
            download_video_with_user_choice_batch(video_url, output_path, default_res)
