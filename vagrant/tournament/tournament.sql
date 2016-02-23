-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
  id    SERIAL PRIMARY KEY,
  name  VARCHAR(50)
);

CREATE TABLE tournaments (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50)
);

CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  tournament_id INT REFERENCES tournaments (id),
  winner_id INT REFERENCES players (id),
  loser_id INT REFERENCES players (id),
  draw BOOLEAN
);

CREATE TABLE results (
	id SERIAL PRIMARY KEY,
	tournament_id INT REFERENCES tournaments (id),
	player_id INT REFERENCES players (id),
	points INT DEFAULT 0,
	matches INT DEFAULT 0,
	bye INT DEFAULT 0
);

-- select p.id as idplayer, p.name, count(winner_id) as ganados from matches m, players p where p.id = m.winner_id group by p.id

-- select p.id as idplayer, p.name, count(winner_id) as ganados from matches m, players p where p.id = m.winner_id group by p.id