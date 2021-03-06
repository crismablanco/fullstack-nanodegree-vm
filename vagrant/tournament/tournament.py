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


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    query = "DELETE FROM players"
    c.execute(query)
    DB.commit()
    DB.close


def deleteTournaments():
    """Remove all the tournaments records from the database."""
    DB = connect()
    c = DB.cursor()
    query = "DELETE FROM tournaments"
    c.execute(query)
    DB.commit()
    DB.close


def registerTournament(name):
    """Adds a tournament to tournament database.
        The function returns the ID of the tournament added
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
    """Returns the number of players currently registered
        on an specific tournament."""
    DB = connect()
    c = DB.cursor()
    query = """SELECT count(player_id) as cp
                FROM tournaments_players
                WHERE tournament_id = %s"""
    c.execute(query, (tournament_id,))
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
    DB.commit()
    DB.close()
    asociatePlayerIntoTournament(lastPlayerAdded, tournament_id)


def asociatePlayerIntoTournament(player_id, tournament_id):
    """
        Adds a player into a tournament.
        The player is already stored on database.

        Args:
            player_id: the id of the player to asociate.
            tournament_id: the id of the tournament.
    """

    DB = connect()
    c = DB.cursor()
    query = "SELECT * FROM players WHERE id = %s"
    c.execute(query, (player_id,))
    exist = c.fetchall()
    if exist == []:
        raise ValueError("The player does not exist on database.")
    query = "SELECT * FROM tournaments WHERE id = %s"
    c.execute(query, (tournament_id,))
    exist = c.fetchall()
    if exist == []:
        raise ValueError("The tournament does not exist on database.")

    query = """SELECT * FROM tournaments_players
                WHERE tournament_id = %s AND player_id = %s"""
    c.execute(query, (tournament_id, player_id,))
    exist = c.fetchall()
    if exist == []:
        query = """INSERT INTO tournaments_players
                (tournament_id, player_id) VALUES (%s, %s)"""
        c.execute(query, (tournament_id, player_id))
        DB.commit()
        print "The player was successfully asociated to the tournament"
    else:
        print "The player is already asociated to the tournament"
    DB.close()


def playerStandings(tournament_id):
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

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
    query = """ SELECT  p.id,
                        p.name,
                        (SELECT COUNT(*) FROM matches m
                            WHERE m.winner_id = p.id
                                AND m.draw = False
                                AND m.tournament_id = %s) AS wins,
                        (SELECT COUNT(*) FROM matches m
                            WHERE m.tournament_id = %s
                                AND (m.winner_id = p.id OR m.loser_id = p.id))
                                    AS matches,
                        (SELECT COUNT(*) FROM matches momw
                            WHERE momw.draw = False
                            AND (momw.winner_id IN
                                (SELECT loser_id
                                    FROM matches m
                                    WHERE m.winner_id = p.id and m.bye = 0
                                    AND m.tournament_id = %s)
                            OR momw.winner_id IN
                                (SELECT winner_id
                                    FROM matches m
                                    WHERE m.loser_id = p.id
                                        AND m.bye = 0
                                        AND m.tournament_id = %s))) AS omw
                        FROM players p LEFT JOIN tournaments_players tp
                            on (p.id = tp.player_id)
                        WHERE tp.tournament_id = %s
                        ORDER BY wins DESC, omw ASC"""

    c.execute(query, (tournament_id, tournament_id, tournament_id, tournament_id, tournament_id,))
    standings = []
    standings = c.fetchall()
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
    DB = connect()
    c = DB.cursor()
    query = """INSERT INTO matches (tournament_id, winner_id, loser_id, draw)
                VALUES (%s,%s,%s,%s)"""
    c.execute(query, (tournament_id, winner, loser, draw))
    DB.commit()
    DB.close()


def doBye(tournament_id, player_id):
    """ Generate a bye on the tournament

    Args:
        tournament_id: the ID of the current tournament
    """
    DB = connect()
    c = DB.cursor()
    query = """INSERT INTO matches (tournament_id, winner_id, loser_id, draw, bye)
                VALUES (%s,%s,%s,%s,%s)"""
    c.execute(query, (tournament_id, player_id, player_id, False, 1,))
    DB.commit()
    DB.close()
    return True


def hasBye(tournament_id, player_id):
    """
    -- THIS IS OPTIONAL --

    check if a player has been already 'bye'

    Args:
        tournament_id: the ID of the current tournament
        player_id: the player to check for the 'bye'

    Returns:
        True if the player already had a bye
        False if not
    """

    DB = connect()
    c = DB.cursor()
    query = """SELECT bye FROM matches
                WHERE tournament_id = %s
                    AND (winner_id = %s OR loser_id = %s)"""
    c.execute(query, (tournament_id, player_id, player_id,))
    playerBye = c.fetchone()[0]
    DB.close()
    if playerBye == 0:
        return False
    else:
        return True


def alreadyPlay(tournament_id, player_id1, player_id2):
    """Prevent rematches between players

    Args:
        tournament_id: the current tournament
        player_id1: the first player to check against player2
        player_id2: second player to check against player1

    Returns:
        True if the players already played before
        False if not
    """
    DB = connect()
    c = DB.cursor()
    query = """SELECT id FROM matches
                WHERE tournament_id = %s
                    AND ((winner_id = %s and loser_id = %s)
                        OR (winner_id = %s and loser_id = %s))"""
    c.execute(query, (tournament_id, player_id1, player_id2, player_id2, player_id1,))
    theyPlayed = c.fetchall()
    DB.close()
    if theyPlayed != []:
        return True
    else:
        return False


def swissPairings(tournament_id):
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Args:
      tournament_id: the ID of the current tournament

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    results = playerStandings(tournament_id)
    pairs = []
    numberOfPlayers = countPlayers(tournament_id)

    """ Here is the BYE zone """
    if numberOfPlayers % 2 != 0:
        i = 0
        byeDone = False
        while not byeDone:
            if results[i][5] == 0:
                doBye(tournament_id, results[i][0])
                results.pop(i)
                byeDone = True
            i += 1
            pass
    """ --------------------"""
    i = 0
    while len(results) >= 1:
            b = 1
            withOpponent = False
            while not withOpponent:
                if not alreadyPlay(tournament_id, results[i][0], results[b][0]):
                    pairs.append((results[i][0], results[i][1], results[b][0], results[b][1]))
                    results.pop(i)
                    results.pop(b-1)
                    withOpponent = True
                b += 1
                pass
    pass
    return pairs
