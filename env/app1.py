from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import os
import customtkinter as ctk
from tkinter import ttk
from pytube import YouTube
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_ngrok2 import run_with_ngrok
import subprocess
import requests
import time




app = Flask(__name__, template_folder="")
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
@socketio.on('download_video')
def download_video():
    url = request.form.get("url")
    resolution = request.form.get("resolution")

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(res=resolution).first()

        output_path = os.path.join("downloads", f"{yt.title}.mp4")
        stream.download(output_path="downloads")

        return jsonify({"status": "success", "message": "Downloaded!"})
        #socketio.emit('download_status', {"status": "success", "message": "Downloaded!"})

    except Exception as e:
        #return jsonify({"status": "error", "message": str(e)})
        socketio.emit('download_status', {"status": "error", "message": str(e)})

def on_progress(stream, chunk, bytes_remaining):
    # Your existing on_progress function...
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_completed = (bytes_downloaded/total_size) * 100

    progress_label.configure(text=str(int(percentage_completed)) + "%")
    progress_label.update()

    #progress_bar.set(float(percentage_completed / 100))
    socketio.emit('progress_update', {'percentage': int(percentage_completed)})

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



if __name__ == '__main__':
    socketio.run(app,debug=True)
