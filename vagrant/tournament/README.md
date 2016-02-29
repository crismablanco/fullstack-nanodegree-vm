# Tournament Planner Project
Project Description:
In this project, you’ll be see a Python module that uses the PostgreSQL
database to keep track of players and matches in a game tournament.

The game tournament will use the Swiss system for pairing up players in each
round: players are not eliminated, and each player should be paired with
another player with the same number of wins, or as close as possible.

This project has two parts: 
- `tournament.sql` the database schema (SQL table definitions),
- `tournament.py`  the code that will use it.
This is a Python and Relational Data Base project where you can handle a
tournament with the Swiss System

Another Extra Functionalities:
- Prevent rematches between players.
- It Doesn't assume an even number of players. If there is an odd number of players, assigns one player a “bye” (skipped round). A bye counts as a free win. A player will not receive more than one bye in a tournament.
- Support games where a draw (tied game) is possible.
- When two players have the same number of wins, the rank is according to OMW (Opponent Match Wins), the total number of wins by players they have played against.
- It support more than one tournament in the database. It distinguish between “a registered player” and “a player who has entered in tournament #123”.

## Introduction
This is a project made for Udacity Nanodegree Program of Full Stack Web Developer. 
You can see it:
[here](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)
It can create a Tournament, Register Players, Register Matches between players,
	create the next round pairs according to their scores and more.
It is the final project of the
[Intro to Relational Databases course](https://www.udacity.com/courses/ud197)


## Requierments
The code has been created using Python 2.7.
It is running inside a Vagrant Machine.
Just run the `tournament_test.py` and it will run a full test of the tournament.
If you edit the file you will be able to create your own tournaments.

## Iside the code
In this project I created a `tournament.py` and a `tournament.sql` that 
	stores the code of the tournament generation and the database:

### tournament.sql:
	Be careful, ths system will drop a tournament existing database
`DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
CREATE TABLE players (...);
CREATE TABLE tournaments (...);
CREATE TABLE tournaments_players (...);
CREATE TABLE matches (...);`

### tournament.py

	Here are the function inside the file:

- `def connect()`: Connect to the PostgreSQL database.  Returns a database connection.
- `def deleteMatches()`: Remove all the match records from the database.
- `def deletePlayers()`: Clear out all the player records from the database.
- `def deleteTournaments()`: Remove all the tournaments records from the database.
- `def registerTournament(name)`: Adds a tournament to tournament database.
The function returns the ID of the tournament added. The database assigns a
unique serial id number for the tournament.
- `def countPlayers(tournament_id)`: Returns the number of players currently
registered on an specific tournament.
- `def registerPlayer(name, tournament_id)`: Adds a player to the tournament by
putting an entry in the database. The database should assign an ID number to the
player. Different players may have the same names but will receive different 
ID numbers.
- `def asociatePlayerIntoTournament(player_id, tournament_id)`: Adds a player
into a tournament. The player is already stored on database.
- `def playerStandings(tournament_id)`: Returns a list of the players and their
win records, sorted by wins. The first entry in the list should be the player in
first place, or a player tied for first place if there is currently a tie.
- `def reportMatch(tournament_id, winner, loser, draw)`: Records the outcome of
a single match between two players.
- `def doBye(tournament_id, player_id)`: Generate a bye on the tournament
- `def hasBye(tournament_id, player_id)`: check if a player has been already 'bye'
- `def alreadyPlay(tournament_id, player_id1, player_id2)`: Prevent rematches between players
- `def swissPairings(tournament_id)`: Returns a list of pairs of players for the
next round of a match. Assuming that there are an even number of players
registered, each player appears exactly once in the pairings.  Each player is
paired with another player with an equal or nearly-equal win record, that is,
a player adjacent to him or her in the standings.


## Contact
For contact send an email to crismablanco@gmail.com

Best Regards
Cristian Blanco