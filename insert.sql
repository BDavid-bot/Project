-- Inserting into Artists Table
INSERT INTO Artists (ArtistID, Name, Genre, Country) VALUES (1, 'Lena Raine', 'Video Game', 'Unknown');
INSERT INTO Artists (ArtistID, Name, Genre, Country) VALUES (2, 'Aaron Cherof', 'Video Game', 'Unknown');

-- Inserting into Albums Table
INSERT INTO Albums (AlbumID, Title, ReleaseDate, ArtistID) VALUES (1, 'Minecraft: Caves & Cliffs (Original Game Soundtrack)', '2021-10-20', 1);
INSERT INTO Albums (AlbumID, Title, ReleaseDate, ArtistID) VALUES (2, 'Minecraft: Tricky Trials (Original Game Soundtrack)', '2024-04-26', 2);

-- Inserting into Songs Table
INSERT INTO Songs (Title, Duration, AlbumID, ArtistID) VALUES ('Infinite Amethyst', 271, 1, 1);
INSERT INTO Songs (Title, Duration, AlbumID, ArtistID) VALUES ('otherside', 195, 1, 1);
INSERT INTO Songs (Title, Duration, AlbumID, ArtistID) VALUES ('Precipice', 299, 2, 2);