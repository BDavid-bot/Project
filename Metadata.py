import json
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3

def read_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  config.json not found!")
        return {}

def read_mp3_metadata(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)

        title = audio.get("TIT2", "Unknown Title")  # Song Title
        artist = audio.get("TPE1", "Unknown Artist")  # Artist Name
        album = audio.get("TALB", "Unknown Album")  # Album Name
        duration = int(audio.info.length) if audio.info else 0  # Duration of the song
        
        # Additional metadata for Artist and Album tables
        country = audio.get("TPE3", "Unknown Country")  # Artist's Country
        release_date = audio.get("TDRC", "Unknown Release Date")  # Album Release Date
        genre = audio.get("TCON", "Unknown Genre")  # Genre of the song

        # Print metadata for debugging
        print(f"\nFile: {file_path}")
        print(f"Title: {title}")
        print(f"Artist: {artist}")
        print(f"Album: {album}")
        print(f"Duration: {duration} seconds")
        print(f"Country: {country}")
        print(f"Release Date: {release_date}")
        print(f"Genre: {genre}\n")

    except Exception as e:
        print(f"Error reading MP3 file '{file_path}': {e}")

def scan_music_folder(music_path):
    if not os.path.exists(music_path):
        print(f"⚠️ The folder {music_path} does not exist!")
        return
    
    # Scan folder for MP3 files
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
