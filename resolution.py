from colorama import init, Fore
from pytubefix import YouTube
from pytubefix.exceptions import (
    AgeRestrictedError,
    ExtractError,
    VideoUnavailable,
    RegexMatchError,
)
from pytubefix.cli import on_progress
init()
# ------------------------------------------------------------------------------------------------------

def get_available_resolutions_fast(video_url):
    yt = YouTube(video_url, on_progress_callback=on_progress)
    streams = yt.streams.filter(adaptive=True).filter(mime_type="video/mp4")

    # -------------------------OLD METHODS---------------------------
    # streams = yt.streams.filter(progressive=True)
    # resolutions = list(set(stream.resolution for stream in streams))
    # print(resolutions)
    # return sorted(resolutions)
    # ----------------------------------------------------------------

    resolutions = []
    for stream in streams:
        resolution = stream.resolution
        if resolution and resolution not in resolutions:
            resolutions.append(resolution)
    return resolutions
# ------------------------------------------------------------------------------------------------------

def get_available_resolutions(video_url):
    try:
        yt = YouTube(video_url, on_progress_callback=on_progress)
        streams = yt.streams.filter(adaptive=True).filter(mime_type="video/webm")
        resolutions = []
        for stream in streams:
            resolution = stream.resolution
            if resolution and resolution not in resolutions:
                resolutions.append(resolution)
        return resolutions
    except RegexMatchError:
        print(f"\n\t\t{Fore.RED}**** Invalid Url ****")
    except KeyboardInterrupt:
        print(f"\n\t\t{Fore.RED}**** Aborting ****")
    except:
        print(f"\n\t\t{Fore.RED}**** Invalid Url ****")