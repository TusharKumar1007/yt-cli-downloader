from pytubefix.exceptions import (
    AgeRestrictedError,
    ExtractError,
    VideoUnavailable,
)
from time import sleep
import os
import re
import ffmpeg
from colorama import init, Fore
from audio import download_audio
from batch import download_batch, fetch_links_from_text_file
from file_handler import clear_file, save_links_to_text_file
from gui_selector import file_gui_selection
from playlist import download_playlist
from single import donwload_single, yt_without_audio
from utility import combine, mp4_to_mp3

init()


# -----------------------------------------------------------------------------------------------------------------


def download_hls_video(hls_url):
    try:
        # Get user-defined file name
        file_name = input("Enter file name: ")
        if not file_name:
            print("Invalid file name. Please provide a valid file name.")
            return
        file_name = re.sub(r"[^\w\s-]", "_", file_name)
        # Construct full file path in the downloads folder
        output_file = os.path.join(
            os.path.expanduser("~"), "Downloads", f"{file_name}.mp4"
        )
        print(f"{Fore.YELLOW}\nDownloading {file_name}...")

        (
            ffmpeg.input(hls_url)
            .output(output_file, c="copy")
            .run(overwrite_output=True, quiet=True)
        )
        print(f"{Fore.CYAN}Downloaded successfully!")
    except ffmpeg.Error as e:
        print(f"{Fore.RED}Invalid Url...")
    except KeyboardInterrupt:
        return print(f"{Fore.YELLOW}\n\t\t**** Aborting Donlwoad ****")


# -----------------------------------------------------------------------------------------------------------------


def main():
    while True:
        print(f"{Fore.LIGHTYELLOW_EX}\n**** You can press Q to quit any time ****\n")

        list_options = [
            "Download only single Video",
            "Download Multiple Videos",
            "Download YouTube Playlist",
            "Download Only audio",
            "Add links to file",
            "Clear Youtube link File data",
            "Convert video(MP4) to Audio(MP3)",
        ]
        adv_options = ["# -> For .m3u8 download", "$ -> Audio and video combiner"]

        for index, choise in enumerate(list_options):
            print(f"{Fore.CYAN}{index+1} --> {Fore.GREEN}{choise}")
        print(f"Enter 0 for advance options")
        main_ans = input("\nEnter Your choice: ").strip()
        if main_ans.lower() == "q":
            break
        if main_ans not in ["1", "2", "3", "4", "5", "6", "7", "#", "$", "0"]:
            print(f"{Fore.RED}Invalid choice. Please try again.")
            continue

        if main_ans == "1":
            try:
                donwload_single()
            except AgeRestrictedError as e:
                print(
                    f"\n\t\t{Fore.RED}**** This video is age-restricted and cannot be downloaded ****"
                )
            except ExtractError as e:
                print(
                    f"\n\t\t{Fore.RED}**** There was an error extracting video data. Please check your network connection ****"
                )
            except VideoUnavailable as e:
                print(
                    f"\n\t\t{Fore.RED}**** This video is not available. It may have been removed or made private ****"
                )
            except Exception as e:
                print(f"\n\t\t{Fore.RED}**** Invalid Url ****{e}")

        elif main_ans == "2":
            try:
                link_lst = fetch_links_from_text_file()
                print("\n\t1--> Download as Video")
                print("\t2--> Download as Audio")

                user_choice = input(
                    "Enter your choice by ,default Audio will be downloaded: "
                )

                if user_choice in ["1", "2"]:
                    if user_choice == "1":
                        download_batch(link_lst)
                    else:
                        default_type_choice = input(
                            "Do You Want to give default Quality(192kbps) for all video (Y/N): "
                        )
                        for link in link_lst:
                            download_audio(link,default_type_choice)
                else:
                    for link in link_lst:
                        download_audio(link)

            except KeyboardInterrupt:
                print(f"\n\t\t{Fore.RED}**** Aborting ****")
            except Exception as e:
                print(f"\n\t\t{Fore.YELLOW}**** Please add links using option 5 ****")
                sleep(2)

        elif main_ans == "3":
            os.system("cls" if os.name == "nt" else "clear")
            print(f"\n\t\t{Fore.YELLOW}**** Make Sure The playlist Is Public ****")
            try:
                download_playlist()
            except KeyboardInterrupt:
                print(f"\n\t\t{Fore.RED}**** Aborting ****")
            except ExtractError as e:
                print(
                    f"\n\t\t{Fore.RED}**** There was an error extracting video data. Please check your network connection ****"
                )
            except VideoUnavailable as e:
                print(
                    f"\n\t\t{Fore.RED}**** This video is not available. It may have been removed or made private ****"
                )
            except:
                print(
                    f"\n{Fore.RED}**** Check your Internet connection and try again ****\n"
                )

        elif main_ans == "4":
            video_url = input("Enter the YouTube video URL: ").strip()
            try:
                print("\n\tIf Audio file time is more than 1hr You Need to Wait a little😄")
                download_audio(video_url,'n')
            except KeyboardInterrupt:
                print(f"\n\t\t{Fore.RED}**** Aborting ****")
            except ExtractError as e:
                print(
                    f"\n\t\t{Fore.RED}**** There was an error extracting video data. Please check your network connection ****"
                )
            except VideoUnavailable as e:
                print(
                    f"\n\t\t{Fore.RED}**** This video is not available. It may have been removed or made private ****"
                )
            except Exception as e:
                print(e)
        elif main_ans == "5":
            save_links_to_text_file()

        elif main_ans == "6":
            try:
                res = clear_file()
                if res:
                    print(f"\n\t\t{Fore.CYAN}**** File clear Succesfully ****\n")
                else:
                    print(
                        f"\n\t\t{Fore.YELLOW}**** Aborting clear. File data is preserved ****\n"
                    )
            except KeyboardInterrupt:
                print(f"\n\t\t{Fore.RED}**** Aborting ****")
            except:
                print(f"\t\t{Fore.BLUE}!!! Try cleaning Manually !!!")

        elif main_ans == "7":
            try:
                file_path, file_name = file_gui_selection()
                mp4_to_mp3(file_path, file_name)
            except KeyboardInterrupt:
                print(f"\n\t\t{Fore.RED}**** Aborting ****")
            except:
                print(f"\t\t{Fore.RED}**** Cannot find the file specified ****\t\t")
        elif main_ans == "#":
            user_input_m3u8 = input("Enter .m3u8 Url: ")
            download_hls_video(user_input_m3u8)
        elif main_ans == "$":
            print(
                f"\t\t{Fore.YELLOW}**** You have now Entered in Video and Audio file combiner ****"
            )
            print(
                f"\n\t\t{Fore.YELLOW}**** Works Only if Video Don't have existing Audio ****"
            )
            user_choice = input(
                f"\n{Fore.GREEN}Do you want to download Youtube video without Audio, Press {Fore.CYAN}y {Fore.GREEN}to continue: "
            ).strip()
            if user_choice.lower() == "y":
                yt_without_audio()
            print(f"\n{Fore.YELLOW}Please select Files using mini graphic Interface")
            video_file_path, video_file_name = file_gui_selection()
            audio_file_path, audio_file_name = file_gui_selection("*.mp3")
            combine(video_file_path, audio_file_path)
        elif main_ans == "0":
            for adv_op in adv_options:
                print(adv_op)


# -----------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n\t\t{Fore.RED}Quitting in 5 seconds ....")
        sleep(5)
