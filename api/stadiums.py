from . import api
from flask import request, session, abort
from db.connection import get_db_connection
from auth.decorators import login_required
from permissions.permission import can_user
from services.stadiums import create_stadium


@api.route('/stadiums/search', methods=['GET'])
def search_stadiums():
    query = request.args.get("q", "").strip()
    userid = session.get("userid")
    tournamentId = request.args.get("tournamentId", "").strip()
    db, cursor = get_db_connection()
    try:
        cursor.execute('SELECT id, name FROM stadiums WHERE tournamentId = %s AND name LIKE %s', (tournamentId, f'%{query}%'))
        stadiums = cursor.fetchall()
        return stadiums
    finally:
        cursor.close()
        db.close()

@api.route('/stadiums/create', methods=['POST'])
@login_required
def create_stadiums():
    data = request.get_json() or {}

    name = data.get("name", "").strip()
    if not name:
        return 'error stadium name required', 400
    tournamentId = data.get('tournamentId')
    team_id = data.get("teamId")
    userid = session.get("userid")
    
    if not tournamentId:
        abort(404)

    if not can_user(userid, 'tournament.create_stadiums', tournamentId):
        abort(403)
    db, cursor = get_db_connection()

    try:
        if team_id:
            cursor.execute(
                'SELECT tournamentId FROM teams WHERE id = %s',
                (team_id,)
            )

            team = cursor.fetchone()

            if not team:
                abort(404)

        create_stadium(db, cursor, name, team_id, tournamentId)

        return {'success': True}, 201

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()

@api.route('/stadiums/recommended', methods=['POST', 'GET'])
@login_required
def recommended_stadiums():
    teamId = request.args.get('teamId')
    userid = session.get('userid')
    db, cursor = get_db_connection()
    try:
        cursor.execute("""
            SELECT * 
            FROM stadiums
            JOIN stadium_teams
                ON stadium_teams.stadiumId = stadiums.id
            WHERE stadium_teams.teamId = %s

        """, (teamId,))
        stadiums = cursor.fetchall()
        return stadiums
    finally:
        cursor.close()
        db.close()