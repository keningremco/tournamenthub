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
    import json

    db, cursor = get_db_connection()

    cursor.execute(
        "SELECT id FROM tournaments WHERE code = %s",
        (tournamentCode,)
    )
    tournament = cursor.fetchone()

    if not tournament:
        cursor.close()
        db.close()
        return []

    tournamentId = tournament["id"]

    cursor.execute("""
        SELECT
            teams.id AS teamId,
            teams.name AS name,
            (
                SELECT JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'gameId', games.id,
                        'score', scores.score,
                        'result', scores.result
                    )
                )
                FROM scores
                JOIN games
                    ON scores.gameId = games.id
                JOIN rounds
                    ON games.roundId = rounds.id
                WHERE rounds.tournamentId = %s
                  AND games.status = 'completed'
                  AND scores.teamId = teams.id
            ) AS games
        FROM teams
        JOIN game_teams
            ON teams.id = game_teams.teamId
        JOIN games
            ON game_teams.gameId = games.id
        JOIN rounds
            ON games.roundId = rounds.id
        WHERE rounds.tournamentId = %s
        GROUP BY teams.id, teams.name
    """, (tournamentId, tournamentId))

    data = cursor.fetchall()
    return data
    leaderboard_unsorted = []

    for teamData in data:
        pts = 0
        GF = 0
        W = 0
        D = 0
        L = 0
        MP = 0

        games = teamData["games"]

        # JSON uit MariaDB omzetten naar een Python-lijst
        if isinstance(games, str):
            games = json.loads(games)

        for game in games or []:
            if game["result"] == "won":
                pts += 3
                W += 1
            elif game["result"] == "draw":
                pts += 1
                D += 1
            elif game["result"] == "lost":
                L += 1

            GF += int(game["score"] or 0)
            MP += 1

        # Voeg ieder team precies één keer toe
        leaderboard_unsorted.append({
            "teamId": teamData["teamId"],
            "team": teamData["name"],
            "mp": MP,
            "w": W,
            "d": D,
            "l": L,
            "gf": GF,
            "ga": None,
            "gd": None,
            "pts": pts
        })

    cursor.close()
    db.close()

    return leaderboard_unsorted

    
