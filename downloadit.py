import tkinter
import customtkinter
from pytube import YouTube
import os

# Function to get the path to the "Downloads" folder
def get_downloads_folder():
    user_profile = os.environ.get('USERPROFILE')
    if user_profile:
        return os.path.join(user_profile, 'Downloads')
    else:
        # Fallback option if USERPROFILE environment variable is not available
        return os.path.join(os.path.expanduser('~'), 'Downloads')

# Function to ensure that the "Downloads" folder exists, creating it if necessary
def ensure_downloads_folder():
    downloads_folder = get_downloads_folder()
    if not os.path.exists(downloads_folder):
        os.makedirs(downloads_folder)

def startVideoDownload():
    try:
        ensure_downloads_folder()  # Ensure that the "Downloads" folder exists
        ytLink = link.get()
        ytObject = YouTube(ytLink, on_progress_callback=on_progress)
        video = ytObject.streams.get_highest_resolution()
        title_text = ytObject.title
        title.configure(text=title_text, text_color="white")
        finishLabel.configure(text="")
        video_file_path = os.path.join(get_downloads_folder(), title_text + '.mp4')
        video.download(filename=video_file_path)
        finishLabel.configure(text="Downloaded!", text_color="white")
    except Exception as e:
        print(e)
        finishLabel.configure(text="Download Error", text_color="red")

def startAudioDownload():
    try:
        ensure_downloads_folder()  # Ensure that the "Downloads" folder exists
        ytLink = link.get()
        ytObject = YouTube(ytLink)
        audio = ytObject.streams.filter(only_audio=True).first()
        title_text = ytObject.title
        title.configure(text=title_text, text_color="white")
        finishLabel.configure(text="")
        audio_file_path = os.path.join(get_downloads_folder(), title_text + '_Audio.mp4')
        out_file = audio.download(filename=audio_file_path)
        finishLabel.configure(text="Audio Downloaded!", text_color="white")
        # save the file 
        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp3'
        os.rename(out_file, new_file) 
    except Exception as e:
        print(e)
        finishLabel.configure(text="Audio Download Error", text_color="red")



def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    per = str(int(percentage_of_completion))
    pPercentage.configure(text=per + '%')
    pPercentage.update()
    progressBar.set(float(percentage_of_completion) / 100)
    app.update_idletasks()  # Force an immediate update of the progress bar

# System Settings
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.geometry("720x320")
app.title("Download It")

# Adding UI Elements with customized appearance and padding
title = customtkinter.CTkLabel(app, text="Insert a Youtube Link", font=("Helvetica", 20, "bold"))
title.pack(padx=10, pady=(20, 10))  # 20 pixels of padding on top, 10 pixels of padding on the bottom

# Link Input
url_var = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=350, height=40, textvariable=url_var)
link.pack()

# Finished Downloading
finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack()

# Progress percentage
pPercentage = customtkinter.CTkLabel(app, text="0%")
pPercentage.pack()
progressBar = customtkinter.CTkProgressBar(app, width=400)
progressBar.set(0)
progressBar.pack(padx=10, pady=10)

# Download Buttons
download = customtkinter.CTkButton(app, text="Download Video (MP4)", command=startVideoDownload)
download.pack(padx=10, pady=5)

audioDownload = customtkinter.CTkButton(app, text="Download Audio (MP3)", command=startAudioDownload)
audioDownload.pack(padx=10, pady=5)

# Run app
app.iconbitmap("D:\Program\Code\DownloadIt\downloadit.ico") 
app.mainloop()
