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
@api.route('/tournament/<tournamentcode>/rounds/<lobbycode>/<userid>')
def get_rounds(tournamentcode, lobbycode=None, userid=None):
    db, cursor = get_db_connection()

    rounds = get_tournament(tournamentcode, cursor, json)

    if lobbycode and userid:
        evals = get_evals(cursor, lobbycode)

        for round in rounds:
            for game in round['games']:
                game_id = game['id']

                # Voeg evaluations toe voor deze game
                game['evaluations'] = evals.get(game_id, {})

                # Zoek de evaluatie van deze gebruiker
                for player in game['evaluations'].get('players', []):
                    if str(player['userId']) == str(userid):
                        game['evaluations']['predictedAway'] = player['predictedUserAway']
                        game['evaluations']['predictedHome'] = player['predictedUserHome']
                        break

    cursor.close()
    db.close()

    return rounds
