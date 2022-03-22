# Clipboard YouTube Downloader
import time
import os
from pytube import YouTube #pip install pytube
import re
import clipboard #pip install pyperclip
import ctypes


def get_clipboard():
    text = clipboard.paste()  # text will have the content of clipboard
    return text

def extract_url(s):
    url = str(re.search("(?P<url>https?://[^\s]+)", s).group("url"))
    return url

def dl_from_clip():
    clip = get_clipboard()
    #check for url
    if "youtube.com/" in clip or "youtu.be/" in clip:
        #check for multiline
        if "\n" in clip:
            #check line for url
            for line in clip.split("\n"):
                if "https://youtube.com/" in line or "https://youtu.be/" in line:
                    youtube_url = extract_url(line)
                    return True, youtube_url
                else:
                    pass
        else:
            youtube_url = extract_url(clip)
            return True, youtube_url
        #still no return, no link found
        for i in range(0, 10):
            clip = str(clip) + "0"
        return False, "empty"
    else:
        return False, ""

def handle_archive(video_id):
    archive_ids = list()
    try:
        f = open("./archive.txt", "r")
        archive_ids = f.readlines()
        f.close()
    except Exception as e:
        print(str(e))
    for archive_id in archive_ids:
        archive_id = archive_id.replace("\n", "")
        if video_id == archive_id:
            return True
    #write not return = no match
    f = open("archive.txt", "a")
    f.write(video_id + "\n")
    f.close()
    return False


def yt_dl_url(yt_url):
    yt = YouTube(yt_url)
    video_id = yt.video_id
    download_status = handle_archive(video_id)
    if download_status == True:
        print("Allready downloaded " + str(yt.title))
    else:
        print("Download: " + str(yt.title))
        streams = yt.streams.all()
        dl_stream = str()
        for stream in streams:
            if "audio/" in str(stream) and 'abr="128kbps"' in str(stream):
                dl_stream = stream
        if not stream == "":
            dl_stream.download("./Downloads/")


ctypes.windll.kernel32.SetConsoleTitleA("YouTube Clipboard2Download")
while True:
    try:
        status, youtube_url = dl_from_clip()
        if status == True:
            yt_dl_url(youtube_url)
        time.sleep(15)
    except Exception as e:
        time.sleep(15)
        pass
exit()

clear_windows = lambda: os.system('cls')
clear_linux = lambda: os.system('clear')
while True:
    print("[YouTube to Clipboard to Audio]")
    print("Watch out clipboard for YouTube links...")
    status, youtube_url = get_from_clipboard()
    if status == True:
        yt_dl_url(youtube_url)
    else:
        "No URL found Sleeping..."
        time.sleep(15)
        clear_windows()
        #clear_linux()
