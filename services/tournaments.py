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