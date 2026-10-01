from . import api
from db.connection import get_db_connection
from services.tournaments import get_game_round

@api.route('/tournament/<tournamentcode>/round/<roundnumber>')
def get_round(tournamentcode, roundnumber):
    db, cursor = get_db_connection()

    games = get_game_round(tournamentcode, roundnumber, cursor)
    
    cursor.close()
    db.close()
    return games

@api.route('/tournament/<tournamentcode>/rounds')
def get_rounds(tournamentcode, roundnumber):
    db, cursor = get_db_connection()

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
                    'awayTeam', (
                                    SELECT teams.name
                                    FROM teams
                                    JOIN game_teams
                                        ON game_teams.teamId = teams.id
                                    WHERE game_teams.home_away = 'away' AND game_teams.gameId = games.id
                                ),
                    'location', stadiums.name
                )
            )
            FROM games
            JOIN stadiums
                ON games.stadiumId = stadiums.id
            WHERE games.roundId = rounds.id
        ) AS games
        FROM rounds
        JOIN tournaments
            ON tournaments.id = rounds.tournamentId
        WHERE tournaments.code = %s
    """)
    rounds = cursor.fetchall()
    cursor.close()
    db.close()
    return rounds