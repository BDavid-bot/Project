import json
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

def read_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("config.json not found!")
        return {}

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

if __name__ == "__main__":
    config = read_config()
    music_path = config.get("music_path")

    if music_path and os.path.exists(music_path):
        # Example: read first MP3 file in the folder
        for file in os.listdir(music_path):
            if file.lower().endswith(".mp3"):
                full_path = os.path.join(music_path, file)
                read_mp3_metadata(full_path)
                break
        else:
            print("No MP3 files found in the specified folder.")
    else:
        print("Invalid or missing music_path in config.json.")
