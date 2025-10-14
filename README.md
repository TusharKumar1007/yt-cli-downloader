# 🎬 YouTube Media Downloader CLI



A command-line YouTube video/audio downloader built with `pytubefix`, `ffmpeg`, and `colorama`. Supports single videos, playlists, audio-only downloads, and more — all with interactive prompts.

---

## 📦 Features

- ✅ Download single YouTube videos
- 📁 Batch download from a saved file
- 📜 Download full YouTube playlists
- 🔊 Audio-only download (e.g., for podcasts or music)
- 🔃 Convert `.mp4` videos to `.mp3`
- 🧩 Combine separate video and audio files
- 🌐 Download `.m3u8` HLS streams
- 🧼 Clear saved video links file
- 💡 GUI selector for choosing files (uses `tkinter`)

---

## 🖥️ Demo

```bash
$ python main_script.py

**** You can press Q to quit any time ****

1 --> Download only single Video
2 --> Download Multiple Videos
3 --> Download YouTube Playlist
4 --> Download Only audio
5 --> Add links to file
6 --> Clear Youtube link File data
7 --> Convert video(MP4) to Audio(MP3)

Enter Your choice:
```

# 📂 Project Structure
```
.
├── audio.py               # Handles YouTube audio-only downloads
├── batch.py               # Batch download logic from text file
├── config.py              # Config settings or constants
├── downloader.py          # Core download logic or shared utilities
├── file_handler.py        # File operations: save, read, clear links
├── gui_selector.py        # GUI-based file picker (likely using tkinter)
├── main.py                # Main CLI entry point with interactive menu
├── playlist.py            # Handles full playlist downloads
├── resolution.py          # Manages video resolution selection
├── single.py              # Single video download (with/without audio)
├── utility.py             # Misc utilities like merging audio/video, conversion

```

# 🔧 Requirements
# Make Sure you have Either chrome web browser or Firefox web browser for the PlayList Functionality to work
# Run this command to download dependency to your envinorment
```bash
pip install -r requirement.txt
```
And install ffmpeg (required for conversion/merging):

# Windows: 
Download [FFmpeg](https://ffmpeg.org/download.html) and add to PATH.

# macOS:
```bash 
brew install ffmpeg
```

# Linux(tested on Fedora 42): 

Enable RPM Fusion free and nonfree repositories:
```bash
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```
Update your package metadata:
```bash
sudo dnf upgrade --refresh
```

Install FFmpeg and development libraries:
```bash
sudo dnf install ffmpeg ffmpeg-devel --allowerasing
```
Verify the installation:
```bash
ffmpeg -version

```

for tkinter use:
```bash
sudo dnf install python3-tkinter
```

# verify Tkinter installation
```bash
python3 -m tkinter
```

# 🚀 Usage
Run the script:
```bash
python main.py
```

You will be prompted with options to choose from:

1: Download a single video

2: Download videos in batch (after adding links via option 5)

3: Download an entire playlist

4: Download only the audio track

5: Add links to a batch file

6: Clear saved link file

7: Convert .mp4 to .mp3


# 📁 Batch Download
Add links using Option 5:
https://youtube.com/watch?v=abc123
https://youtube.com/watch?v=xyz456

Then run Option 2 to batch download them.

# 🧪 Advanced
.m3u8 (HLS) streams supported via ffmpeg
Combiner mode allows merging separate video and audio files into one .mp4

# ❗ Error Handling
The script gracefully handles:

Network issues
Age restrictions
Missing or invalid videos
Keyboard interrupts

# 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

# 🙏 Credits

pytubefix

ffmpeg-python

colorama


# If you only want the app,there is a google drive link, download the Dragon.zip, extract it, run Dragon.exe.
I update the app every month so there is no issue. Complete App Exe file --> https://drive.google.com/drive/folders/18mim94kirQuN-BGICr5J94y7tOoDG9mw?usp=sharing
