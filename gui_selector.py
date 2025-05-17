import tkinter as tk
from tkinter import filedialog
import os
# ------------------------------------------------------------------------------------------------------

def file_gui_selection(file_extention="*.mp4"):
    root = tk.Tk()
    root.title("File Selection")
    file_path = None
    file_name = None

    if file_extention == "*.mp4":
        file_type = "MP4"
        file_type_name = "Video"
    else:
        file_type = "MP3"
        file_type_name = "Audio"

    def open_file_dialog():
        nonlocal file_path, file_name
        file_path = filedialog.askopenfilename(
            filetypes=[(f"{file_type} files", f"{file_extention}")]
        )
        print("Selected file:", file_path)
        file_path = file_path.replace("/", "\\")
        file_name = os.path.splitext(os.path.basename(file_path))[0]
        root.destroy()

    button = tk.Button(
        root, text=f"Select {file_type_name} File", command=open_file_dialog
    )
    button.pack(pady=20)
    root.mainloop()
    return file_path, file_name