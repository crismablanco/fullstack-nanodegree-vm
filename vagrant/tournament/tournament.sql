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

-- THE NEXT TABLE IS USED TO STORE THE PLAYERS REGISTERED ON A TOURNAMENT
-- PLAYERS CAN BE REGISTERED BUT WITHOUT MATCHES YET.
-- IT DOESN'T NEED A PRIMARY KEY
CREATE TABLE tournaments_players (
  player_id INT REFERENCES players (id) ON DELETE CASCADE,
  tournament_id INT REFERENCES tournaments (id) ON DELETE CASCADE
);

CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  tournament_id INT REFERENCES tournaments (id) ON DELETE CASCADE,
  winner_id INT REFERENCES players (id) ON DELETE CASCADE,
  loser_id INT REFERENCES players (id) ON DELETE CASCADE,
  draw BOOLEAN,
  bye INT DEFAULT 0
);
