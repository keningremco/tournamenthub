from . import api
from db.connection import get_db_connection
from services.tournaments import get_game_round, get_tournament
from services.lobbies import get_evals
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
def get_rounds(tournamentcode, lobbycode=None, userid=None):
    db, cursor = get_db_connection()
    rounds = get_tournament(tournamentcode, cursor, json)
    if lobbycode and userid:
        evals = get_evals(cursor, lobbycode)
        counter = 0
        counter2 = 0
        for round in rounds:
            for game in round['games']:
                rounds[counter]['games'][counter2]['evaluations'] = evals.get(game['id'], [])
                for player in rounds[counter]['games'][counter2]['evaluations']['players']:
                    if player['userId'] == userid:
                        rounds[counter]['games'][counter2]['evaluations']['predictedAway'] = player['predictedUserAway']
                        rounds[counter]['games'][counter2]['evaluations']['predictedHome'] = player['predictedUserHome']
                counter2 =+ 1
            counter =+ 1
    cursor.close()
    db.close()
    return rounds