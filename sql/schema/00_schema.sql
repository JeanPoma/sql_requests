-- Création du schéma pour dataset RAWG (normalisé)
CREATE DATABASE IF NOT EXISTS vg;
USE vg;

CREATE TABLE platforms(
  id INT PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(50) NOT NULL,
  UNIQUE KEY uq_platform (code)
);

CREATE TABLE genres(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  UNIQUE KEY uq_genre (name)
);

CREATE TABLE publishers(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  UNIQUE KEY uq_publisher (name)
);

CREATE TABLE developers(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  UNIQUE KEY uq_developer (name)
);

CREATE TABLE tags(
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  UNIQUE KEY uq_tag (name)
);

CREATE TABLE games(
  id INT PRIMARY KEY AUTO_INCREMENT,
  rawg_id INT NULL,
  name VARCHAR(255) NOT NULL,
  released DATE NULL,
  year SMALLINT NULL,
  metacritic SMALLINT NULL CHECK (metacritic BETWEEN 0 AND 100),
  rating DECIMAL(4,2) NULL,
  ratings_count INT NULL,
  playtime INT NULL,
  esrb VARCHAR(50) NULL,
  KEY idx_games_year (year),
  KEY idx_games_name (name)
);

CREATE TABLE game_platforms(
  game_id INT NOT NULL,
  platform_id INT NOT NULL,
  PRIMARY KEY(game_id, platform_id),
  FOREIGN KEY (game_id) REFERENCES games(id),
  FOREIGN KEY (platform_id) REFERENCES platforms(id),
  KEY idx_gp_platform (platform_id)
);

CREATE TABLE game_genres(
  game_id INT NOT NULL,
  genre_id INT NOT NULL,
  PRIMARY KEY(game_id, genre_id),
  FOREIGN KEY (game_id) REFERENCES games(id),
  FOREIGN KEY (genre_id) REFERENCES genres(id)
);

CREATE TABLE game_publishers(
  game_id INT NOT NULL,
  publisher_id INT NOT NULL,
  PRIMARY KEY(game_id, publisher_id),
  FOREIGN KEY (game_id) REFERENCES games(id),
  FOREIGN KEY (publisher_id) REFERENCES publishers(id)
);

CREATE TABLE game_developers(
  game_id INT NOT NULL,
  developer_id INT NOT NULL,
  PRIMARY KEY(game_id, developer_id),
  FOREIGN KEY (game_id) REFERENCES games(id),
  FOREIGN KEY (developer_id) REFERENCES developers(id)
);

CREATE TABLE game_tags(
  game_id INT NOT NULL,
  tag_id INT NOT NULL,
  PRIMARY KEY(game_id, tag_id),
  FOREIGN KEY (game_id) REFERENCES games(id),
  FOREIGN KEY (tag_id) REFERENCES tags(id)
);
