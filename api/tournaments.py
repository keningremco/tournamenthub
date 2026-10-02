from . import api
from db.connection import get_db_connection
from services.tournaments import get_game_round, get_tournament
from api.lobbies import getLobbyEvaluations
import json

@api.route('/tournament/<tournamentcode>/round/<roundnumber>')
def get_round(tournamentcode, roundnumber):
    db, cursor = get_db_connection()

    games = get_game_round(tournamentcode, roundnumber, cursor)
    
    cursor.close()
    db.close()
    return games

@api.route('/tournament/<tournamentcode>/rounds')
@api.route('/tournament/<tournamentcode>/rounds/<lobbycode>')
def get_rounds(tournamentcode, lobbycode=None):
    db, cursor = get_db_connection()
    rounds = get_tournament(tournamentcode, cursor, json)
    if lobbycode:
        evals = getLobbyEvaluations(lobbycode)
        for round in rounds:
            for game in round['games']:
                game['evaluations'] = evals[game['id']]