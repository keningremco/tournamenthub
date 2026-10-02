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