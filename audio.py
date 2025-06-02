import inspect
import re
from colorama import init, Fore
from pytubefix import YouTube
import os
from pytubefix.cli import on_progress

import ffmpeg
from config import ffmpeg_path
from config import repl_output_path, mach_output_path

init()

# ----------------------------------------old code--------------------------------------------------------------

# def download_audio(url):
#     yt = YouTube(url, on_progress_callback=on_progress)

#     audio_stream = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
#     yt_title = audio_stream.title

#     if "REPLIT_ENVIRONMENT" in os.environ:
#         output_path = "./downloads"
#     else:

#         output_path = os.path.join(os.path.expanduser("~"), "Downloads")
#     yt_title = re.sub(r'[<>:"/\\|?*\']', "", yt_title)

#     caller = inspect.stack()[1].function

#     if caller not in ["download_video_with_user_choice_single"]:
#         print(f"\n{Fore.MAGENTA}Downloading {yt_title} as Audio...\n ")
#     audio_stream.download(output_path=output_path, filename=f"{yt_title}.mp3")
#     if caller not in ["download_video_with_user_choice_single"]:
#         print(f"{Fore.CYAN}**** Audio Download Complete ****\n")


caller = inspect.stack()[1].function


def save_audio(stream_audio, output_path, yt_title):

    # Temporary filename (source format)
    source_ext = stream_audio.mime_type.split("/")[-1]
    temp_file = os.path.join(output_path, f"{yt_title}_temp.{source_ext}")
    final_file = os.path.join(output_path, f"{yt_title}.mp3")

    print('\tDO NOT PANIC IF IT LOOKS STUCK')
    stream_audio.download(output_path=output_path, filename=os.path.basename(temp_file))
    

    # Convert to MP3 using the custom ffmpeg path
    try:
        (
            ffmpeg.input(temp_file)
            .output(final_file, format="mp3", audio_bitrate="192k")
            # .output(
            #     final_file,
            #     format="mp3",
            #     audio_bitrate="192k",
            #     threads=4,  # Use multiple threads
            #     **{"compression_level": "0"},
            # )
            .overwrite_output()
            .run(cmd=ffmpeg_path, quiet=True)
        )
        os.remove(temp_file)
    except Exception as e:
        print(f"{Fore.RED}Failed to convert to mp3: {e}")
        return

    # Success message
    if caller not in ["download_video_with_user_choice_single"]:
        print(f"{Fore.CYAN}**** Audio Download Complete ****\nSaved to: {final_file}")


def download_audio(url, default_type_choice):
    yt = YouTube(url, on_progress_callback=on_progress)

    # Filter and sort audio streams
    audio_streams = yt.streams.filter(only_audio=True).order_by("abr").desc()

    # Sanitize title
    yt_title = re.sub(r'[<>:"/\\|?*\']', "", yt.title)

    # Output path
    if "REPLIT_ENVIRONMENT" in os.environ:
        output_path = repl_output_path

    else:
        output_path = mach_output_path

    default_stream = None
    for stream in audio_streams:
        if stream.abr == "128kbps" and "mp4a.40.2" in (stream.audio_codec or ""):
            default_stream = stream
            break

    if default_type_choice.lower() == "n":

        print(f"\n{Fore.GREEN}Available Audio Qualities for: {yt_title}\n")
        for idx, stream in enumerate(audio_streams, start=1):
            print(
                f"{Fore.YELLOW}[{idx}] {stream.abr} - {stream.mime_type} - {stream.audio_codec}"
            )

        # Get user input
        while True:
            try:
                choice = input(
                    f"\n{Fore.CYAN}Enter the number of the quality you want to download: "
                )

                if choice == "q":
                    break
                selected_stream = audio_streams[int(choice) - 1]
                break
            except (ValueError, IndexError):
                print(f"{Fore.RED}Invalid choice. Please try again.")

        # Inform user
        if caller not in ["download_video_with_user_choice_single"]:
            print(
                f"\n{Fore.MAGENTA}Downloading {yt_title} ({selected_stream.abr})...\n"
            )

        save_audio(selected_stream, output_path, yt_title)

    if default_type_choice.lower() == "q":
        return

    if default_type_choice.lower() == "y":
        if default_stream is None:
            print(
                f"{Fore.RED}No suitable default stream found (128kbps AAC). Aborting."
            )
            return

        selected_stream = default_stream
        print(
            f"\n{Fore.MAGENTA}Downloading {yt_title} ({selected_stream.abr}) using default...\n"
        )
        save_audio(selected_stream, output_path, yt_title)

        # source_ext = selected_stream.mime_type.split("/")[-1]
        # temp_file = os.path.join(output_path, f"{yt_title}_temp.{source_ext}")
        # final_file = os.path.join(output_path, f"{yt_title}.mp3")

        # selected_stream.download(output_path=output_path, filename=os.path.basename(temp_file))

        # # Convert to MP3 using the custom ffmpeg path
        # try:
        #     (
        #         ffmpeg
        #         .input(temp_file)
        #         .output(final_file, format='mp3', audio_bitrate='192k')
        #         .overwrite_output()
        #         .run(cmd=ffmpeg_path, quiet=True)
        #     )
        #     os.remove(temp_file)
        # except Exception as e:
        #     print(f"{Fore.RED}Failed to convert to mp3: {e}")
        #     return

        # if caller not in ["download_video_with_user_choice_single"]:
        #     print(f"{Fore.CYAN}**** Audio Download Complete ****\nSaved to: {final_file}")
    else:return