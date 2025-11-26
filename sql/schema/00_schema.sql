-- Création du schéma pour dataset RAWG (normalisé) - PostgreSQL version

-- Tables de référence
CREATE TABLE platforms(
  id SERIAL PRIMARY KEY,
  code VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE genres(
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE publishers(
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE developers(
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE tags(
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE
);

-- Table principale : games
CREATE TABLE games(
  id SERIAL PRIMARY KEY,
  rawg_id INT NULL,
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) NULL,
  released DATE NULL,
  year SMALLINT NULL,
  metacritic SMALLINT NULL CHECK (metacritic BETWEEN 0 AND 100),
  rating DECIMAL(4,2) NULL,
  ratings_count INT NULL,
  playtime INT NULL,
  esrb VARCHAR(50) NULL
);

-- Index sur games pour performance
CREATE INDEX idx_games_year ON games(year);
CREATE INDEX idx_games_name ON games(name);
CREATE INDEX idx_games_slug ON games(slug);

-- Tables de liaison (many-to-many)
CREATE TABLE game_platforms(
  game_id INT NOT NULL,
  platform_id INT NOT NULL,
  PRIMARY KEY(game_id, platform_id),
  FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
  FOREIGN KEY (platform_id) REFERENCES platforms(id) ON DELETE CASCADE
);
CREATE INDEX idx_gp_platform ON game_platforms(platform_id);

CREATE TABLE game_genres(
  game_id INT NOT NULL,
  genre_id INT NOT NULL,
  PRIMARY KEY(game_id, genre_id),
  FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
  FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE
);

CREATE TABLE game_publishers(
  game_id INT NOT NULL,
  publisher_id INT NOT NULL,
  PRIMARY KEY(game_id, publisher_id),
  FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
  FOREIGN KEY (publisher_id) REFERENCES publishers(id) ON DELETE CASCADE
);

CREATE TABLE game_developers(
  game_id INT NOT NULL,
  developer_id INT NOT NULL,
  PRIMARY KEY(game_id, developer_id),
  FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
  FOREIGN KEY (developer_id) REFERENCES developers(id) ON DELETE CASCADE
);

CREATE TABLE game_tags(
  game_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(game_id, tag_id),
  FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
