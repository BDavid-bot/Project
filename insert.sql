-- Inserting into Users Table
INSERT INTO Users (Username, Email, JoinDate) VALUES 
('john_doe', 'john@example.com', '03-30-2025'),
('jane_smith', 'jane@example.com', '03-28-2025'),
('alice_brown', 'alice@example.com', '03-25-2025'),
('bob_white', 'bob@example.com', '03-22-2025');

-- Inserting into Artists Table
INSERT INTO Artists (Name, Genre, Country) VALUES 
('The Wanderers', 'Rock', 'USA'),
('SynthWave', 'Electronic', 'Germany'),
('Soul Harmony', 'R&B', 'UK'),
('Acoustic Bliss', 'Folk', 'Canada');

-- Inserting into Albums Table
INSERT INTO Albums (Title, ReleaseDate, ArtistID) VALUES 
('Road to Nowhere', '2024-05-10', 1),
('Electric Dreams', '2023-08-15', 2),
('Smooth Vibes', '2022-02-20', 3),
('Campfire Songs', '2023-11-11', 4);

-- Inserting into Songs Table
INSERT INTO Songs (Title, Duration, AlbumID) VALUES 
('Nowhere Fast', 210, 1),
('Dream Machine', 180, 2),
('Heart & Soul', 195, 3),
('Morning Light', 165, 4),
('Wanderlust', 240, 1),
('Neon Nights', 200, 2),
('Harmony Lane', 210, 3),
('Fireside Stories', 175, 4);
