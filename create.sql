-- Users Table
-- Functional Dependency: UserID → Username, Email, JoinDate
CREATE TABLE IF NOT EXISTS Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    JoinDate TEXT
);

-- Artists Table
-- Functional Dependency: ArtistID → Name, Genre, Country
CREATE TABLE IF NOT EXISTS Artists (
    ArtistID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Genre TEXT,
    Country TEXT
);

-- Albums Table
-- Functional Dependency: AlbumID → Title, ReleaseDate, ArtistID
CREATE TABLE IF NOT EXISTS Albums (
    AlbumID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    ReleaseDate TEXT,
    ArtistID INTEGER,
    FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID) ON DELETE CASCADE
);

-- Songs Table
-- Functional Dependency: SongID → Title, Duration, AlbumID
CREATE TABLE IF NOT EXISTS Songs (
    SongID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Duration INTEGER,
    AlbumID INTEGER,
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID) ON DELETE CASCADE
);
