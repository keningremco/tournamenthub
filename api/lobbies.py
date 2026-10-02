from flask import request, jsonify, flash
from auth.decorators import login_required
from . import api
from db.connection import get_db_connection
from services.lobbies import get_lobby_leaderboard, get_evals

@api.route("/lobbies/public")
@login_required
def public_lobbies():
    tournament_code = request.args.get("tournament_code", "").strip().upper()
    if not tournament_code:
        return []

    db, cursor = get_db_connection()

    try:
        cursor.execute(
            """
            SELECT tournaments.name, tournaments.name AS tournament_name, lobbies.code AS code, COUNT(lobby_members.userId) AS member_count
            FROM `tournaments`
            JOIN lobbies ON lobbies.tournamentId = tournaments.id
            JOIN lobby_members ON lobby_members.lobbyId = lobbies.id
            WHERE tournaments.code = %s AND lobbies.isPrivate = 'public'
            GROUP BY lobbies.id
            
            """,
            (
                tournament_code,
            )
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()

@api.route("/lobby/<lobbyCode>/evaluations")
def getLobbyEvaluations(lobbyCode):

    db, cursor = get_db_connection()

    try:

        evaluationData = get_evals(cursor, lobbyCode)


        return jsonify(evaluationData)


    finally:

        cursor.close()
        db.close()



@api.route('/lobby/code/<code>/leaderboard')
@api.route('/lobby/id/<int:id>/leaderboard')
def api_get_lobby_leaderboard(code=None, id=None):
    db, cursor = get_db_connection()
    
    leaderboard, status, error_code = get_lobby_leaderboard(lobbyId=id, lobbyCode=code, cursor=cursor)

    cursor.close()
    db.close()

    if status == 'error':
        error_msg = leaderboard
        flash(error_msg, 'error')
        return error_msg, error_code

    
    return leaderboard, 200