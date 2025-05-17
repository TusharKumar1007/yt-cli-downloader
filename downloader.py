import re, os
from colorama import init, Fore
from http.client import IncompleteRead
from pytubefix import YouTube
from pytubefix.exceptions import (
    AgeRestrictedError,
    ExtractError,
    VideoUnavailable,
    RegexMatchError,
)
from pytubefix.cli import on_progress

from audio import download_audio
from utility import combine, delete_files_with_name, determine_output_path
from config import retry_count

from tqdm import tqdm
import time


init()

# ------------------------------------------------------------------------------------------------------


def initilise_progress_bar(video_stream, audio_stream):
    global start_time, pbar
    start_time = time.time()
    pbar = tqdm(
        total=video_stream.filesize + audio_stream.filesize,
        unit="B",
        unit_scale=True,
        desc="Downloading",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{rate_fmt}] {postfix}",
        dynamic_ncols=True,
        position=0,
        mininterval=0.1,
    )


# ------------------------------------------------------------------------------------------------------
def on_progress(stream, chunk: bytes, bytes_remaining: int):
    """
    This callback is triggered during the download. It calculates the download speed and updates the progress bar.
    """
    global start_time, pbar
    bytes_downloaded = stream.filesize - bytes_remaining
    download_speed = bytes_downloaded / (
        time.time() - start_time
    )  # in bytes per second
    download_speed_mbps = download_speed / 1_000_000  # convert to Mbps

    progress = (bytes_downloaded / stream.filesize) * 100
    pbar.update(len(chunk))

    # Update the progress bar with download speed and remaining size
    pbar.set_postfix(
        {
            # "Speed": f"{download_speed_mbps:.2f} Mbps",
            "Remaining": f"{bytes_remaining / 1_000_000:.2f} MB",
        }
    )


# ------------------------------------------------------------------------------------------------------


def download_video_with_user_choice_single_fast(video_url, resolution):
    global retry_count
    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)

        # Attempt to get the adaptive video and audio streams
        video_stream = yt.streams.filter(
            adaptive=True, mime_type="video/mp4", resolution=resolution
        ).first()
        audio_stream = yt.streams.filter(adaptive=True, mime_type="audio/mp4").first()

        # Check if both video and audio streams were found
        if not video_stream or not audio_stream:
            print(
                f"\n{Fore.RED}No suitable video or audio stream found for resolution {resolution}."
            )
            return None

        # Get the title of the video
        title = video_stream.title

        video_filesize_bytes = video_stream.filesize
        video_filesize_mb = video_filesize_bytes / (1024 * 1024)  # Convert bytes to MB

        # Get the size of the audio stream (if available)
        audio_filesize_bytes = audio_stream.filesize
        audio_filesize_mb = audio_filesize_bytes / (1024 * 1024)  # Convert bytes to MB

        # Total size (video + audio)
        total_filesize_mb = video_filesize_mb + audio_filesize_mb

        # Clean the title to make it safe for file naming
        title = re.sub(r'[<>:"/\\|?*\']', "", title)

        # Determine the output path based on the environment
        output_path = determine_output_path()

        # Download video and audio to files
        print(f"\n{Fore.MAGENTA}Downloading {title} {total_filesize_mb:.2f} MB....")

        initilise_progress_bar(video_stream, audio_stream)

        video_file = os.path.join(output_path, f"{title}.mp4")
        audio_file = os.path.join(output_path, f"{title}.mp3")

        # Download video and audio streams
        video_stream.download(output_path=output_path, filename=f"{title}.mp4")
        audio_stream.download(output_path=output_path, filename=f"{title}.mp3")

        # Close progress bar after download completes
        pbar.close()

        # Combine the video and audio streams
        combine(video_file, audio_file)

        # Clean up the files
        output_path = determine_output_path()
        delete_files_with_name(output_path, title)

        print(f"{Fore.CYAN}Download completed successfully!\n")

        # Save the video URL and title to a file
        with open("temp_links.txt", "a+") as f:
            f.write(f"{title} --> {video_url}\n")

        return title

    except IncompleteRead:
        retry_count += 1
        if retry_count <= 2:
            print(
                f"\n\t\t{Fore.RED}**** Incomplete Download. Retrying download... ****"
            )
            return download_video_with_user_choice_single_fast(video_url, resolution)
        else:
            print(
                f"\n\t\t{Fore.RED}Try downloading {title} Url:{video_url} using option 1..."
            )
    except KeyboardInterrupt:
        pbar.close()
        print(f"\n\t\t{Fore.RED}**** Aborting ****")

    except Exception as e:
        pbar.close()
        print(f"\nError: {e}")
        return None
    finally:
        # Ensure the progress bar is closed when all is done or an exception occurs
        pbar.close()


# ------------------------------------------------------------------------------------------------------


def download_video_with_user_choice_single(video_url, resolution):
    global retry_count
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

        try:
            yt = YouTube(video_url, on_progress_callback=on_progress)
            stream = yt.streams.filter(
                adaptive=True, mime_type="video/webm", resolution=resolution
            )
            if stream:
                video = stream.first()
                audio_stream = (
                    yt.streams.filter(only_audio=True).order_by("abr").desc().first()
                )

                filesize_bytes = video.filesize
                filesize_mb = filesize_bytes / (1024 * 1024)
                output_path = determine_output_path()
                title = yt.title
                print(
                    f"{Fore.MAGENTA}Downloading {title} in {resolution} resolution {filesize_mb:.2f} MB..."
                )

                initilise_progress_bar(video, audio_stream)
                title = re.sub(r'[<>:"/\\|?*\']', "", title)

                video.download(output_path=output_path, filename=f"{title}.mp4")
                audio_stream.download(output_path=output_path, filename=f"{title}.mp3")

                pbar.close()

                path = f"{output_path}/{title}.mp4"

                """
                not using th audio downloading fuction , it interfare with progress bar byut keeping it in reference

                """
                # download_audio(video_url)
                # print(f"Audio: {output_path}/{title}.mp3", path)

                combine(path, f"{output_path}/{title}.mp3")

                delete_files_with_name(output_path, title)

                print(f"{Fore.CYAN}Video downloaded successfully!\n")
                with open("temp_links.txt", "a+") as f:
                    f.write(f"{title} --> {video_url}\n")
                return title, 0
            else:
                print(f"{Fore.RED}No video found for the selected resolution.")
                return "No title", 404
        except IncompleteRead:
            retry_count += 1
            if retry_count <= 3:
                print(
                    f"\n\t\t{Fore.RED}**** Incomplete Donwload. Retrying download... ****"
                )
                return download_video_with_user_choice_single_fast(
                    video_url, output_path, resolution="720p"
                )
            else:
                return print(
                    f"\n\t\t{Fore.RED}Try downloading {title} Url:{video_url} using option 1..."
                )
        except (UnicodeEncodeError, UnicodeDecodeError) as e:
            # print("Error: ", e)
            return title, 0
        except RegexMatchError:
            print(f"\n\t\t{Fore.RED}**** Invalid Url ****")
        except KeyboardInterrupt:
            pbar.close()
            print(f"\n\t\t{Fore.RED}**** Aborting ****")
        except Exception as e:
            pbar.close()
            print("Error:", e)
            return title, 404
