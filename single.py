import os
import re
from downloader import (
    download_video_with_user_choice_single,
    download_video_with_user_choice_single_fast,
)
from resolution import get_available_resolutions, get_available_resolutions_fast
from colorama import init, Fore
from pytubefix import YouTube
from pytubefix.cli import on_progress
from utility import determine_output_path, open_mp4_file

init()
# ------------------------------------------------------------------------------------------------------


def donwload_single():
    video_url = input("Enter Video Url: ").strip()
    output_path = os.path.join(os.path.expanduser("~"), "Downloads\\")
    choice_lst = [
        "Blazing Fast download(Limited Resolutions)",
        "Fast Download(More fps and Resolutons)",
    ]

    for i, x in enumerate(choice_lst):
        print(f"\t\t{i+1} --> {x}")

    fast_moreres_choice = input("Enter your choice: ").strip()

    if fast_moreres_choice == "1":
        resolutions = get_available_resolutions_fast(video_url)
    else:
        resolutions = get_available_resolutions(video_url)

    if not resolutions:
        return print(
            f"\n\t\t{Fore.RED}**** This video might be recently uploaded.Try after 24 Hours or Try using option 1--> Blazing fast ****"
        )
    print(f"\n{Fore.YELLOW}Available resolutions:")
    for i, resolution in enumerate(resolutions):
        print(f"{i + 1}. {resolution}")

    try:
        choice = input(
            "Enter the number corresponding to the desired resolution: "
        ).strip()

        if choice.isdigit():
            choice = int(choice)
        else:
            raise Exception

        if choice <= 0:
            raise IndexError
        selected_resolution = resolutions[choice - 1]
    except KeyboardInterrupt:
        print(f"\n\t\t{Fore.RED}**** Aborting ****")
    except IndexError:
        return print(f"\n\t\t{Fore.RED}**** Invalid choice ****")
    except Exception:
        return print(f"\n\t\t{Fore.RED}**** Enter correct Information ****")

    if fast_moreres_choice == "1":
        yt_title = download_video_with_user_choice_single_fast(
            video_url, selected_resolution
        )
    else:
        try:
            yt_title, return_code = download_video_with_user_choice_single(
                video_url, selected_resolution
            )
        except Exception as e:
            return

        video_file_path = os.path.join(output_path, f"{yt_title}z.mp4")

        open_video = input(
            f"Do you want to Play video now press {Fore.CYAN}1 {Fore.GREEN}to play or any other key to leave: "
        ).strip()

        if open_video == "1":
            try:
                open_mp4_file(video_file_path)
            except KeyboardInterrupt:
                print(f"\n\t\t{Fore.RED}**** Aborting ****")
            except Exception as e:
                print(e)
            except:
                print(
                    f"{Fore.RED}There is an error opening the file... Try opening manually"
                )


# ------------------------------------------------------------------------------------------------------


def yt_without_audio():
    try:

        video_url = input("Enter Video Url: ").strip()
        output_path = os.path.join(os.path.expanduser("~"), "Downloads\\")
        resolutions = get_available_resolutions(video_url)
        if not resolutions:
            return print(
                f"\n\t\t{Fore.RED}**** This video might be recently uploaded.Try after 24 Hours or Try using option 1--> Blazing fast ****"
            )
        print(f"\n{Fore.YELLOW}Available resolutions:")
        for i, resolution in enumerate(resolutions):
            print(f"{i + 1}. {resolution}")

        try:
            choice = input(
                "Enter the number corresponding to the desired resolution: "
            ).strip()

            if choice.isdigit():
                choice = int(choice)
            else:
                raise Exception

            if choice <= 0:
                raise IndexError
            selected_resolution = resolutions[choice - 1]
        except KeyboardInterrupt:
            print(f"\n\t\t{Fore.RED}**** Aborting ****")
        except IndexError:
            return print(f"\n\t\t{Fore.RED}**** Invalid choice ****")
        except Exception:
            return print(f"\n\t\t{Fore.RED}**** Enter correct Information ****")

        if resolution in [
            "1080p",
            "720p",
            "480p",
            "360p",
            "240p",
            "144p",
            "1440p",
            "2160p",
            "4320p",
        ]:

            yt = YouTube(video_url, on_progress_callback=on_progress)
            stream = yt.streams.filter(
                adaptive=True, mime_type="video/webm", resolution=selected_resolution
            )
            if stream:
                video = stream.first()
                filesize_bytes = video.filesize
                filesize_mb = filesize_bytes / (1024 * 1024)
                output_path = determine_output_path()
                title = yt.title
                print(
                    f"{Fore.MAGENTA}Downloading {title} in {selected_resolution} resolution {filesize_mb:.2f} MB..."
                )
                title = re.sub(r'[<>:"/\\|?*\']', "", title)

                video.download(output_path=output_path, filename=f"{title}.mp4")

                path = f"{output_path}/{title}.mp4"

        os.path.join(output_path, f"{title}z.mp4")
        print(f"\n\t\t{Fore.CYAN}**** Download successful ****")
    except KeyboardInterrupt:
        print(f"\n\t\t{Fore.RED}**** Aborting ****")
    except Exception as e:
        print(f"\n\t\t{Fore.RED}**** Error: {e} ****")
