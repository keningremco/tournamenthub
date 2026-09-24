from . import api
from db.connection import get_db_connection
from auth.decorators import login_required
from flask import session, request, abort
from permissions.permission import can_user

@api.route("/teams/create", methods=["POST"])
@login_required
def create_team():
    userid = session.get("userid")

    data = request.get_json()
    tournamentId = data.get('tournamentId')
    if not tournamentId:
        abort(404)
    if not can_user(userid, 'tournament.create_team', tournamentId):
        abort(403)
    name = data.get("name", "").strip()

    if not name:
        return {"error": "Team name is required"}, 400

    if len(name) > 100:
        return {"error": "Team name is too long"}, 400

    db, cursor = get_db_connection()

    try:
        # Check of deze gebruiker al een team met deze naam heeft
        cursor.execute("""
            SELECT id
            FROM teams
            WHERE tournamentId = %s
              AND name = %s
        """, (tournamentId, name))

        existing_team = cursor.fetchone()

        if existing_team:
            return {
                "error": "You already have a team with this name"
            }, 409

        # Team maken
        cursor.execute("""
            INSERT INTO teams (name, tournamentId)
            VALUES (%s, %s)
        """, (name, tournamentId))

        db.commit()

        return {
            "id": cursor.lastrowid,
            "name": name
        }, 201

    finally:
        cursor.close()
        db.close()

@api.route('/teams/search', methods=['GET', "POST"])
def search_teams():
    query = request.args.get('q')
    tournamentId = request.args.get('tournamentId')
    db, cursor = get_db_connection()

    try:
        cursor.execute("SELECT * FROM teams WHERE tournamentId = %s AND name LIKE %s", (tournamentId,f'%{query}%'))
        teams = cursor.fetchall()
        return teams
    finally:
        cursor.close()
        db.close()