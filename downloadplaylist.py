# YouTube Playlist Downloader
#
# Asks the user for a YouTube playlist URL and downloads all the videos in the playlist.
# Before download, the user is asked for a choice of Audio or Video.
# If they choose video, save as .mp4
# If they choose audio, save as .mp3

import os
import subprocess
import sys

# try import yt_dlp, and install it if it's not found
try:
    import yt_dlp
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'yt-dlp'])
    import yt_dlp

# find out clear screen command for OS
if os.name == "nt":
    clear = "cls"
else:
    clear = "clear"

audioOnly = False
playlistName = ""

while True:
    # ask user for playlist URL
    playlist_url = input("Enter the URL of the YouTube playlist\n> ")

    # check if URL is valid
    if "youtube.com/playlist" in playlist_url:
        # don't download anything, just get the playlist name
        output = subprocess.getstatusoutput(f"yt-dlp --quiet -s -o '%(playlist)s' --max-downloads 1 --get-filename "
                                            + playlist_url)
        if output[0] == 0 or output[0] == 101:
            playlistName = output[1]
            print(f"Found playlist: {playlistName}\n")
            break
    else:
        print("Error getting playlist\n")
        continue

# check if URL is a YouTube Music playlist, and assume audio only if it is
if "music.youtube.com/playlist" in playlist_url:
    audioOnly = True
else:
    # ask user if they want to download audio or video
    while True:
        choice = input("Download audio or video?\n> ")
        if choice.lower() == "audio":
            audioOnly = True
            break
        elif choice.lower() == "video":
            audioOnly = False
            break
        else:
            print("Invalid choice\n")
            continue

# download playlist

# video command:
# # yt-dlp --quiet -o playlistName/%(title)s.%(ext)s' --format mp4 <playlist>

# audio command:
# # yt-dlp --quiet -o playlistName/%(title)s.%(ext)s' --format bestaudio --extract-audio --audio-format mp3 <playlist>

# run these while showing the yt-dlp output

print("Downloading playlist...")
if audioOnly:
    subprocess.run(f"yt-dlp --quiet -o '{playlistName}/%(title)s.%(ext)s' --format bestaudio --extract-audio "
                   f"--audio-format mp3 " + playlist_url, shell=True)
else:
    subprocess.run(f"yt-dlp --quiet -o '{playlistName}/%(title)s.%(ext)s' --format mp4 " + playlist_url, shell=True)


# print success message
print("Download complete")
