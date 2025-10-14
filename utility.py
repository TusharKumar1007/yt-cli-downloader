from colorama import init, Fore
import inspect
import os
import ffmpeg
from config import ffmpeg_path
import platform
import re
from config import repl_output_path, mach_output_path
from gui_selector import file_gui_selection
import subprocess


init()

# ------------------------------------------------------------------------------------------------------


def combine(video, audio):
    caller = inspect.stack()[1].function
    # print('test1')

    if "REPLIT_ENVIRONMENT" in os.environ:
        output_path = repl_output_path
    else:
        # Default output path for other environments
        output_path = mach_output_path

    # print('test2')
    output_filename = os.path.splitext(os.path.basename(video))[0] + "z.mp4"
    # print('test3')
    output_path = os.path.join(output_path, output_filename)
    # print('test4')
    # ------------Using FFMPEG----------
    input_video = ffmpeg.input(video)
    # print('test5')
    input_audio = ffmpeg.input(audio)
    # print('test6')
    # print(input_audio)
    # print(input_video)
    # print(output_path)

    # print(ffmpeg_path)
    ffmpeg.output(
        input_video, input_audio, output_path, codec="copy"
    ).overwrite_output().run(ffmpeg_path, quiet=True)
    if caller == "main":
        print(f"\n\t\t{Fore.MAGENTA}**** Sucessfully Combined Audio And Video ****")


# ------------------------------------------------------------------------------------------------------


def mp4_to_mp3(file_path, file_name="audio.mp3"):
    if file_path.strip() in [None, ""]:
        return print("\n\t\t**** No file Selected ****\n")

    user_option = [
        "Convert with high speed,same quality as in video",
        "Convert to best quality 320Kpbs",
    ]

    print("\n")
    for index, choice in enumerate(user_option):
        print(f"\t\t{Fore.CYAN}{index+1} --> {Fore.GREEN}{choice}")

    print("\n")

    user_choice = ""
    while user_choice not in ["1", "2"]:
        user_choice = input("Enter Your choice, press q to exit: ").strip()
        if user_choice.lower() == "q":
            return

    output_filename = (
        input(
            "Enter name for audio file, press enter to auto detect file name: "
        ).strip()
        + ".mp3"
    )

    if output_filename in [None, ".mp3"]:
        output_filename = file_name + ".mp3"
    try:
        if file_path is None:
            print(f"\n{Fore.RED}***** No file selected *****")
            return
        output_dir = os.path.expanduser("~\\Downloads")
        if platform.system() == "Linux":
            output_dir = os.path.expanduser("~/Downloads")
        output_path = os.path.join(output_dir, output_filename)
        if user_choice == "1":
            print(f"\n\t\t{Fore.MAGENTA}**** Conversion in progress Normal ****\n")

            (
                ffmpeg.input(file_path)
                .output(output_path, format="mp3", acodec="libmp3lame")
                .run(ffmpeg_path, overwrite_output=True, quiet=True)
            )
        else:
            print(f"\n\t\t{Fore.MAGENTA}**** Conversion in progress (320Kbps) ****\n")

            (
                ffmpeg.input(file_path)
                .output(
                    output_path, format="mp3", acodec="libmp3lame", audio_bitrate="320k"
                )
                .run(ffmpeg_path, overwrite_output=True, quiet=True)
            )
        print(f"{Fore.CYAN}Conversion completed successfully!")
    except KeyboardInterrupt:
        print(f"\n\t\t{Fore.RED}**** Aborting ****")
    except ffmpeg.Error as e:
        print(f"{Fore.RED}An error occurred: {e.stderr}")


# ------------------------------------------------------------------------------------------------------


def open_mp4_file(file_path):
    if platform.system() == "Windows":
        # print(file_path)
        os.startfile(file_path)
    elif platform.system() == "Linux":
        file_path = file_path.replace("\\", "/")
        subprocess.run(["xdg-open", file_path])


def delete_files_with_name(downloads_folder, file_prefix):

    files = os.listdir(downloads_folder)

    pattern = re.compile(rf"{re.escape(file_prefix)}\.(mp4|mp3)$", flags=re.IGNORECASE)

    for file in files:

        if pattern.match(file):

            file_path = os.path.join(downloads_folder, file)
            try:

                os.remove(file_path)
                # print(f"Deleted file: {file}")
            except Exception as e:
                # print(f"{Fore.RED}Error deleting file: {file}. Reason: {e}")
                print(f"{Fore.RED}Skipping delete ")


# ------------------------------------------------------------------------------------------------------


def determine_output_path():
    # Check if the code is running on Replit
    if "REPLIT_ENVIRONMENT" in os.environ:
        return "./downloads"
    else:
        return os.path.join(os.path.expanduser("~"), "Downloads")


# ------------------------------------------------------------------------------------------------------


def uptune_audio():
    print("\n\tPlease select the file from gui")
    (full_path, file_name) = file_gui_selection("*.mp3")

    # print(f"{full_path}\n{file_name}")

    output_path = os.path.join(determine_output_path(), f"{file_name}_192kbps.mp3")
    try:
        if not full_path:
            raise FileNotFoundError(f"\t{Fore.RED}❌ Please select a file")

        print(f"{Fore.CYAN}UpTunning {file_name}")

        (
            ffmpeg.input(full_path)
            .output(output_path, audio_bitrate="192k", acodec="libmp3lame")
            .overwrite_output()
            .run(quiet=True)
        )
        print(f"{Fore.GREEN}✅ File re-encoded to 192k and saved at: {output_path}")
    except FileNotFoundError as e:
        print(e)
    except ffmpeg.Error as e:
        print(f"{Fore.RED}❌ FFmpeg error:", e)
