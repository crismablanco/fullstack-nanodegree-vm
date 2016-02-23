#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    query = "DELETE FROM matches"
    c.execute(query)
    DB.commit()
    DB.close
    

def deleteResults():
    """Remove all the result records from the database."""
    DB = connect()
    c = DB.cursor()
    query = "DELETE FROM results"
    c.execute(query)
    DB.commit()
    DB.close


def deletePlayers():
    """Remove all the player records from the database."""
    deleteResults()
    deleteMatches()
    DB = connect()
    c = DB.cursor()
    query = "DELETE FROM players"
    c.execute(query)
    DB.commit()
    DB.close


def deleteTournaments():
    """Remove all the tournaments records from the database."""
    deleteResults()
    deleteMatches()
    DB = connect()
    c = DB.cursor()
    query = "DELETE FROM tournaments"
    c.execute(query)
    DB.commit()
    DB.close


def registerTournament(name):
    """Adds a tournament to tournament database. the function returns the ID of the tournament added
  
    The database assigns a unique serial id number for the tournament.
  
    Args:
      name: the tournament's name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    query = "INSERT INTO tournaments (name) VALUES (%s) RETURNING id"
    c.execute(query, (name,))
    lastTournamentAdded = c.fetchone()[0]
    DB.commit()
    DB.close()
    return lastTournamentAdded
    
def countPlayers(tournament_id):
    """Returns the number of players currently registered on an specific tournament."""
    DB = connect()
    c = DB.cursor()
    query = "SELECT count(player_id) as cp FROM results WHERE tournament_id = %s"
    c.execute(query,(tournament_id,))
    countP = c.fetchone()[0]
    DB.close()
    return countP

def registerPlayer(name, tournament_id):
    """Adds a player into a tournament to tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      tournament_id: the tournament's ID where to register the player
    """
    DB = connect()
    c = DB.cursor()
    query = "INSERT INTO players (name) VALUES (%s) RETURNING id"
    c.execute(query, (name,))
    lastPlayerAdded = c.fetchone()[0]
    query = "INSERT INTO results (tournament_id, player_id, points, matches, bye) VALUES (%s, %s, %s, %s, %s)"
    c.execute(query, (tournament_id,lastPlayerAdded,0,0,0))
    DB.commit()
    DB.close()
    

def playerStandings(tournament_id):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Args:
      tournament_id: the tournament ID for the standings.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    query = """SELECT r.player_id, p.name, r.points, r.matches, r.bye, 
                (SELECT SUM(r2.points)
                     FROM results AS r2
                     WHERE r2.player_id IN (SELECT loser_id
                                     FROM matches m
                                     WHERE m.winner_id = r.player_id
                                     AND m.tournament_id = %s)
                     OR r2.player_id IN (SELECT winner_id
                                 FROM matches m
                                 WHERE m.loser_id = r.player_id
                                 AND m.tournament_id = %s)) AS pointsOthers
                 FROM results r, players p
                 WHERE r.tournament_id = %s AND p.id = r.player_id
                 ORDER BY r.points DESC, pointsOthers ASC, r.matches DESC"""
    c.execute(query, (tournament_id, tournament_id, tournament_id))
    standings = []
    for row in c.fetchall():
        standings.append(row)
    DB.close()
    return standings


def reportMatch(tournament_id, winner, loser, draw):
    """Records the outcome of a single match between two players.

    Args:
      tournament_id: the ID of the current tournament
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      draw: true or false as appropiate
    """
    
    if draw == 'TRUE':
        pointsOfWinner = 1
        pointsOfLoser = 1
    else:
        pointsOfWinner = 3
        pointsOfLoser = 0

    DB = connect()
    c = DB.cursor()
    query = "INSERT INTO matches (tournament_id, winner_id, loser_id, draw) VALUES (%s,%s,%s,%s)"
    winnerUpdate = "UPDATE results SET points = points+%s, matches = matches+1 WHERE tournament_id = %s AND player_id = %s"
    loserUpdate = "UPDATE results SET points = points+%s, matches = matches+1 WHERE tournament_id = %s AND player_id = %s"
    c.execute(query, (tournament_id, winner, loser, draw))
    c.execute(winnerUpdate, (pointsOfWinner, tournament_id, winner))
    c.execute(loserUpdate, (pointsOfLoser, tournament_id, loser))
    DB.commit()
    DB.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


