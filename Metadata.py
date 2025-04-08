import json
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.id3 import TIT2, TPE1, TALB, TDRC, TCON, TXXX

def read_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  config.json not found!")
        return {}

def safe_str(tag):
    return str(tag.text[0]) if tag and tag.text else "Unknown"

def read_mp3_metadata(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)
        tags = audio.tags

        title = safe_str(tags.get("TIT2"))
        artist = safe_str(tags.get("TPE1"))
        album = safe_str(tags.get("TALB"))
        year = safe_str(tags.get("TDRC"))
        genre = safe_str(tags.get("TCON"))
        country = safe_str(tags.get("TXXX:Country"))  # Custom field
        duration = int(audio.info.length) if audio.info else 0

        return {
            "title": title,
            "artist": artist,
            "album": album,
            "year": year,
            "genre": genre,
            "country": country,
            "duration": duration
        }

    except Exception as e:
        print(f"Error reading MP3 file '{file_path}': {e}")
        return None

def scan_music_folder_and_generate_sql(music_path):
    artists = {}
    albums = {}
    songs = []
    artist_id_counter = 1
    album_id_counter = 1

    for root, _, files in os.walk(music_path):
        for file in files:
            if file.lower().endswith(".mp3"):
                full_path = os.path.join(root, file)
                metadata = read_mp3_metadata(full_path)

                if metadata:
                    artist_name = metadata["artist"]
                    if artist_name not in artists:
                        artists[artist_name] = {
                            "id": artist_id_counter,
                            "genre": metadata["genre"],
                            "country": metadata["country"]
                        }
                        artist_id_counter += 1

                    album_key = (metadata["album"], artist_name)
                    if album_key not in albums:
                        albums[album_key] = {
                            "id": album_id_counter,
                            "year": metadata["year"],
                            "artist_id": artists[artist_name]["id"]
                        }
                        album_id_counter += 1

                    songs.append({
                        "title": metadata["title"],
                        "duration": metadata["duration"],
                        "album_id": albums[album_key]["id"],
                        "album_title": metadata["album"],
                        "artist_name": artist_name  # Add artist name for reference
                    })

    return generate_insert_sql(artists, albums, songs)

def generate_insert_sql(artists, albums, songs):
    lines = []

    # Artists
    lines.append("-- Inserting into Artists Table")
    for name, data in artists.items():
        lines.append(
            f"INSERT INTO Artists (ArtistID, Name, Genre, Country) VALUES "
            f"({data['id']}, '{name.replace("'", "''")}', '{data['genre'].replace("'", "''")}', '{data['country'].replace("'", "''")}');"
        )

    # Albums
    lines.append("\n-- Inserting into Albums Table")
    for (album_title, artist_name), data in albums.items():
        lines.append(
            f"INSERT INTO Albums (AlbumID, Title, ReleaseDate, ArtistID) VALUES "
            f"({data['id']}, '{album_title.replace("'", "''")}', '{data['year']}', {data['artist_id']});"
        )

    # Songs
    lines.append("\n-- Inserting into Songs Table")
    for song in songs:
        # Add the ArtistID here, which can be found in the albums dictionary based on the album_id
        album_id = song['album_id']
        artist_id = albums[(song['album_title'], song['artist_name'])]['artist_id']  # Retrieve the ArtistID from the album

        lines.append(
            f"INSERT INTO Songs (Title, Duration, AlbumID, ArtistID) VALUES "
            f"('{song['title'].replace("'", "''")}', {song['duration']}, {album_id}, {artist_id});"
        )

    return "\n".join(lines)

def save_insert_sql(content, output_path="insert.sql"):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ insert.sql written with generated SQL statements.")
    except Exception as e:
        print(f"❌ Failed to write insert.sql: {e}")

if __name__ == "__main__":
    config = read_config()
    music_path = config.get("music_path")

    if music_path:
        sql_content = scan_music_folder_and_generate_sql(music_path)
        save_insert_sql(sql_content)
    else:
        print("Invalid or missing music_path in config.json.")
