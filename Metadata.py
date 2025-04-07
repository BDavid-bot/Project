import json
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

# Reads data from the config file
def read_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("config.json not found!")
        return {}

# Gets title, artist, album and duration from the file's metadata & prints it to the console
def read_mp3_metadata(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)

        title = audio.get("TIT2", "Unknown Title")
        artist = audio.get("TPE1", "Unknown Artist")
        album = audio.get("TALB", "Unknown Album")
        duration = int(audio.info.length) if audio.info else 0

        print(f"\nFile: {file_path}")
        print(f"Title: {title}")
        print(f"Artist: {artist}")
        print(f"Album: {album}")
        print(f"Duration: {duration} seconds\n")

    except Exception as e:
        print(f"Error reading MP3 file '{file_path}': {e}")

# Recursively scans the folder from config to display all MP3s
def scan_music_folder(music_path):
    if not os.path.exists(music_path):
        print(f"The folder {music_path} does not exist!")
        return
    
    for root, _, files in os.walk(music_path):
        for file in files:
            if file.lower().endswith(".mp3"):
                full_path = os.path.join(root, file)
                read_mp3_metadata(full_path)

if __name__ == "__main__":
    config = read_config()
    music_path = config.get("music_path")

    if music_path:
        scan_music_folder(music_path)
    else:
        print("Invalid or missing music_path in config.json.")
