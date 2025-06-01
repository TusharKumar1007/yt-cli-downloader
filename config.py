import os
import sys

# ------------------------------------------------------------------------------------------------------

retry_count = 0

# use this when creating an .exe
bundle_dir = getattr(sys, "_MEIPASS", os.path.abspath(os.path.dirname(__file__)))
ffmpeg_relative_path = os.path.join(r"ffmpeg.exe")
ffmpeg_path = os.path.abspath(os.path.join(bundle_dir, ffmpeg_relative_path))

# for reminder
# ffmpeg_relative_path = os.path.join(r"C:\ffmpeg_for_python\ffmpeg.exe")

# use this when in vs code
# ffmpeg_path = os.path.join(r"C:\ffmpeg_for_python\ffmpeg.exe")

# ----output Paths-----
mach_output_path = os.path.join(os.path.expanduser("~"), "Downloads") #machine outputpath
repl_output_path = "./downloads" #repl output path

