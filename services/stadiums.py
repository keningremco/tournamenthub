def create_stadium(db, cursor, name, teamid, tournamentId):
    try:
        cursor.execute(
            'INSERT INTO stadiums (tournamentId, name) VALUES (%s, %s)',
            (tournamentId, name)
        )

        stadiumid = cursor.lastrowid

        if teamid:
            cursor.execute(
                'INSERT INTO stadium_teams (stadiumId, teamId) VALUES (%s, %s)',
                (stadiumid, teamid)
            )

        db.commit()

    except Exception:
        db.rollback()
        raise