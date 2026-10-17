from db.connection import get_db_connection
import json


def get_game_round(tournamentcode, roundnumber, cursor):

    cursor.execute("""
        SELECT 
            games.id AS gameId,
            games.status AS status,
            games.start_time AS start_time,
            rounds.*,
            stadiums.*,
            (
                SELECT teams.name
                FROM teams
                JOIN game_teams
                    ON game_teams.teamId = teams.id
                WHERE game_teams.gameId = games.id AND game_teams.home_away = 'home'
            ) AS home_team,
            (
                SELECT teams.name
                FROM teams
                JOIN game_teams
                    ON game_teams.teamId = teams.id
                WHERE game_teams.gameId = games.id AND game_teams.home_away = 'away'
            ) AS away_team,
            (
                SELECT scores.score
                FROM scores
                JOIN game_teams
                    ON games.id = game_teams.gameId
                WHERE scores.gameId = games.id AND scores.teamId = game_teams.teamId AND game_teams.home_away = 'home'
            ) AS home_score,
            (
                SELECT scores.score
                FROM scores
                JOIN game_teams
                    ON games.id = game_teams.gameId
                WHERE scores.gameId = games.id AND scores.teamId = game_teams.teamId AND game_teams.home_away = 'away'
            ) AS away_score
        FROM games
        JOIN rounds
            ON games.roundId = rounds.id
        JOIN tournaments
            ON rounds.tournamentId = tournaments.id
        JOIN stadiums
            ON stadiums.id = games.stadiumId
        WHERE tournaments.code = %s AND rounds.roundNumber = %s
        ORDER BY games.start_time
    
    """, (tournamentcode, roundnumber))
    games = cursor.fetchall()
    return games


def get_tournament(tournamentcode, cursor, json):
    
    cursor.execute("""
        SELECT 
        rounds.*,
        (
            SELECT JSON_ARRAYAGG(
                JSON_OBJECT(
                    'id', games.id,
                    'roundId', games.roundId,
                    'homeTeam', (
                                    SELECT teams.name
                                    FROM teams
                                    JOIN game_teams
                                        ON game_teams.teamId = teams.id
                                    WHERE game_teams.home_away = 'home' AND game_teams.gameId = games.id
                                ),
                    'homeTeamId', (
                                    SELECT teams.id
                                    FROM teams
                                    JOIN game_teams
                                        ON game_teams.teamId = teams.id
                                    WHERE game_teams.home_away = 'home' AND game_teams.gameId = games.id
                                ),
                    'awayTeam', (
                                    SELECT teams.name
                                    FROM teams
                                    JOIN game_teams
                                        ON game_teams.teamId = teams.id
                                    WHERE game_teams.home_away = 'away' AND game_teams.gameId = games.id
                                ),
                    'awayTeamId', (
                                    SELECT teams.id
                                    FROM teams
                                    JOIN game_teams
                                        ON game_teams.teamId = teams.id
                                    WHERE game_teams.home_away = 'away' AND game_teams.gameId = games.id
                                ),
                    'homeScore', (
                                    SELECT scores.score
                                    FROM scores
                                    JOIN game_teams
                                        ON game_teams.teamId = scores.teamId
                                    WHERE scores.gameId = games.id 
                                    AND game_teams.gameId = games.id
                                    AND game_teams.home_away = 'home'
                                ),
                    'awayScore', (
                                    SELECT scores.score
                                    FROM scores
                                    JOIN game_teams
                                        ON game_teams.teamId = scores.teamId
                                    WHERE scores.gameId = games.id 
                                    AND game_teams.gameId = games.id
                                    AND game_teams.home_away = 'away'
                                ),
                    'location', stadiums.name,
                    'status', games.status,
                    'start-date', games.start_time

                )
            )
            FROM games
            LEFT JOIN stadiums
                ON games.stadiumId = stadiums.id
            WHERE games.roundId = rounds.id
        ) AS games
        FROM rounds
        JOIN tournaments
            ON tournaments.id = rounds.tournamentId
        WHERE tournaments.code = %s
    """, (tournamentcode,))
    rounds = cursor.fetchall()
    for round in rounds:
        if round["games"]:
            round["games"] = json.loads(round["games"])
        else:
            round["games"] = []
    return rounds

def get_tournament_leaderboard(tournamentCode):
    db, cursor = get_db_connection()

    cursor.execute('SELECT id FROM tournaments WHERE code = %s', (tournamentCode))
    tournamentId = cursor.fetchone()

    cursor.execute("""
        SELECT 

            (
                SELECT JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'gameId', games.id,
                        'status', games.status,
                        'score', scores.score,
                        'result', scores.result
                    )
                )
                FROM scores
                JOIN games
                    ON scores.gameId = games.id
                JOIN rounds
                    ON games.roundId = rounds.id
                WHERE games.status = 'completed' AND scores.teamId = teams.id
            ) AS games,
            teams.name

        FROM teams
        JOIN game_teams
            ON teams.id = game_teams.teamId
        JOIN games
            ON game_teams.gameId = games.id
        JOIN rounds
            ON games.roundId = rounds.id
        WHERE rounds.tournamentId = %s
    """, (tournamentId,))

    data = cursor.fetchall()
    leaderboard_unsorted = []
    for teamData in data:
        pts = 0
        GF = 0
        W = 0
        D = 0
        L = 0
        MP = 0

        if isinstance(games, str):
            games = json.loads(games)

        for games in teamData:
            if games['result'] == 'won':
                pts += 3
                W += 1
            elif games['result'] == 'draw':
                pts += 1
                D += 1
            else:
                L += 1
            GF += int(games['score'])
            MP += 1
            leaderboard_unsorted.append({
                "teamName": teamData["name"],
                "pts": pts,
                "GF": GF,
                "W": W,
                "D": D,
                "L": L,
                "MP": MP
            })
    return leaderboard_unsorted



    
