-- Create Operations

-- Add a new user
INSERT INTO Users (Username, Email, JoinDate) VALUES 
('charlie_miller', 'charlie@example.com', '03-29-2025');

-- Add a new artist
INSERT INTO Artists (Name, Genre, Country) VALUES 
('Indie Beats', 'Indie', 'Australia');

-- Add a new album
INSERT INTO Albums (Title, ReleaseDate, ArtistID) VALUES 
('Sunlit Roads', '2025-03-01', 5);

-- Add a new song
INSERT INTO Songs (Title, Duration, AlbumID) VALUES 
('Winding Paths', 220, 5);

-- Read Operations

-- Get all users
SELECT * FROM Users;

-- Get songs along with album and artist info (joined view)
SELECT s.Title AS SongTitle, s.Duration, a.Title AS AlbumTitle, ar.Name AS ArtistName
FROM Songs s
JOIN Albums a ON s.AlbumID = a.AlbumID
JOIN Artists ar ON a.ArtistID = ar.ArtistID;

-- Update Operations

-- Update a user's email
UPDATE Users
SET Email = 'john_d_new@example.com'
WHERE Username = 'john_doe';

-- Update an artist's genre
UPDATE Artists
SET Genre = 'Alternative'
WHERE Name = 'The Wanderers';

-- Update an album title
UPDATE Albums
SET Title = 'Dreamscape'
WHERE Title = 'Electric Dreams';

-- Update a song's duration
UPDATE Songs
SET Duration = 205
WHERE Title = 'Neon Nights';

-- Delete Operations

-- Delete a user by username
DELETE FROM Users
WHERE Username = 'bob_white';

-- Delete an artist by name
DELETE FROM Artists
WHERE Name = 'Acoustic Bliss';

-- Delete an album by title
DELETE FROM Albums
WHERE Title = 'Campfire Songs';

-- Delete a song by title
DELETE FROM Songs
WHERE Title = 'Fireside Stories';
