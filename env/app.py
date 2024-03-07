import customtkinter as ctk
from tkinter import ttk
from pytube import YouTube
import os
from flask import Flask
from flask import Flask, render_template, jsonify, request
from flask_ngrok2 import run_with_ngrok
import subprocess
import requests
import time


def download_video():
    url = entry_url.get()
    resolution = resolutions_var.get()

    progress_label.pack(pady=(10, 5))
    progress_bar.pack(pady=(10, 5))
    status_label.pack(pady=(10, 5))

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(res=resolution).first()

        #Download the video into specific directory
        os.path.join("downloads", f"{yt.title}.mp4")
        stream.download(output_path="downloads")

        status_label.configure(text="Downloaded!", text_color="white", fg_color="green")

    except Exception as e:
        status_label.configure(text=f"Error {str(e)}", text_color="white", fg_color="red")


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = (bytes_downloaded/total_size) * 100

    progress_label.configure(text=str(int(percentage_completed)) + "%")
    progress_label.update()

    progress_bar.set(float(percentage_completed / 100))



#create a root window
root = ctk.CTk()
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#title of the window
root.title("YouTube Downloader!")

#Set min and max width and height
root.geometry("720x480")
root.minsize(720, 480)
root.maxsize(1080, 720)

#create a frame to hold the content
content_frame = ctk.CTkFrame(root)
content_frame.pack(fill=ctk.BOTH,expand=True, padx=10, pady=10)

#create a label and the entry widget for the video url
url_label = ctk.CTkLabel(content_frame, text="Enter the YouTube url : ")
entry_url = ctk.CTkEntry(content_frame, width=400, height=40)
url_label.pack(pady=(10, 5))
entry_url.pack(pady=(10, 5))

#create a download button
download_button = ctk.CTkButton(content_frame, text="Download", command=download_video)
download_button.pack(pady=(10, 5))

#create a resolutions combo box
resolutions = ["1080p", "720p", "480p", "360p", "240p", "144p"]
resolutions_var = ctk.StringVar()
resolution_combobox = ttk.Combobox(content_frame, values=resolutions, textvariable=resolutions_var)
resolution_combobox.pack(pady=(10, 5))
resolution_combobox.set("360p")   #Default setting


#create a label and the progress bar to display the download progress
progress_label = ctk.CTkLabel(content_frame, text="0%")

progress_bar = ctk.CTkProgressBar(content_frame, width=400)
progress_bar.set(0)    #Default setting

#create the status label
status_label = ctk.CTkLabel(content_frame, text="")



#run_with_ngrok(app=app, auth_token="2dLc5CIPzTT97F46VyAFsOATQol_4pZPkX2zhG54aE6nsyHoJ")  # Start ngrok when app is run

app = Flask(__name__)
@app.route("/")
def hello_world():
    return "Namaste"
    


#ngrok = subprocess.Popen(['ngrok', 'http', '8000'])
#ngrok = subprocess.Popen(['env/Scripts/ngrok-asgi.exe', 'http', '8000'])
#app = Flask(__name__, template_folder="app.py", static_folder="")


#To start the App
#root.mainloop()
if __name__ == '__main__':
    app.run()