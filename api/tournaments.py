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