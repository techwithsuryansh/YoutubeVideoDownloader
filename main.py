import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp

def start_download():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    folder = filedialog.askdirectory()
    if not folder:
        return

    # Run download in background thread
    threading.Thread(target=download_video, args=(url, folder), daemon=True).start()


def progress_hook(d):
    if d['status'] == 'downloading':
        try:
            percent = d['_percent_str']
            percent_value = float(percent.replace('%', '').strip())
            progress_bar['value'] = percent_value
            status_label.config(text=f"Downloading... {percent}")
        except:
            pass

    elif d['status'] == 'finished':
        progress_bar['value'] = 100
        status_label.config(text="Download finished. Merging...")


def download_video(url, folder):
    try:
        ydl_opts = {
            "outtmpl": f"{folder}/%(title)s.%(ext)s",
            "progress_hooks": [progress_hook],
            "format": "best"

        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        status_label.config(text="Done!")
        messagebox.showinfo("Success", "Download Completed!")

    except Exception as e:
        messagebox.showerror("Error", f"{e}")
        status_label.config(text="Error")


# GUI
app = tk.Tk()
app.title("YouTube Video Downloader")
app.geometry("550x300")
app.config(bg="#1e1e1e")

title_label = tk.Label(app, text="YouTube Video Downloader",
                       font=("Arial", 18), bg="#1e1e1e", fg="white")
title_label.pack(pady=10)

url_entry = tk.Entry(app, width=55, font=("Arial", 12))
url_entry.pack(pady=5)

download_btn = tk.Button(app, text="Download", bg="#4CAF50", fg="white",
                         font=("Arial", 12), command=start_download)
download_btn.pack(pady=10)

progress_bar = ttk.Progressbar(app, orient="horizontal",
                               length=400, mode="determinate")
progress_bar.pack(pady=10)

status_label = tk.Label(app, text="", bg="#1e1e1e", fg="lightgray")
status_label.pack()


app.mainloop()