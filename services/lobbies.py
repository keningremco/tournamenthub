def get_lobby_rounds_points(lobby_id,userId, cursor):
    cursor.execute("""
        SELECT rounds.id, SUM(predictions.points) AS points
        FROM lobbies
        JOIN tournaments
            ON tournaments.id = lobbies.tournamentId
        LEFT JOIN rounds
            ON rounds.tournamentId = tournaments.id
        LEFT JOIN games
            ON games.roundId = rounds.id
        LEFT JOIN predictions
            ON predictions.gameId = games.id
        WHERE predictions.userId = %s AND lobbies.id = %s
        GROUP BY rounds.id
    """,(userId, lobby_id) )
    rounds_points = cursor.fetchall()
    return rounds_points

def calc_prediction_points_game(gameId, userId, cursor, lobbyId=None):
    cursor.execute("""
        SELECT 
        (
            SELECT ps.score
            FROM game_teams gt
            JOIN predicted_scores ps
                ON ps.teamId = gt.teamId
            WHERE gt.gameId = games.id
            AND ps.predictionId = predictions.id
            ORDER BY gt.id
            LIMIT 1
        ) AS pre_home,

        (
            SELECT ps.score
            FROM game_teams gt
            JOIN predicted_scores ps
                ON ps.teamId = gt.teamId
            WHERE gt.gameId = games.id
            AND ps.predictionId = predictions.id
            ORDER BY gt.id
            LIMIT 1 OFFSET 1
        ) AS pre_uit,

        (
            SELECT s.score
            FROM game_teams gt
            JOIN scores s
                ON s.teamId = gt.teamId
            AND s.gameId = gt.gameId
            WHERE gt.gameId = games.id
            ORDER BY gt.id
            LIMIT 1
        ) AS echt_home,

        (
            SELECT s.score
            FROM game_teams gt
            JOIN scores s
                ON s.teamId = gt.teamId
            AND s.gameId = gt.gameId
            WHERE gt.gameId = games.id
            ORDER BY gt.id
            LIMIT 1 OFFSET 1
        ) AS echt_uit,

        games.id AS game_id

    FROM predictions
    JOIN games
        ON predictions.gameId = games.id

    WHERE predictions.userId = %s
    AND games.id = %s;
    """, (userId, gameId))
    game = cursor.fetchone()

    points = None
    if lobbyId:
        cursor.execute("""
            SELECT *
            FROM lobby_points_rules
            WHERE lobbyId = %s
            LIMIT 1
        """, (lobbyId,))
        points = cursor.fetchone()
    if not lobbyId or not points:
            cursor.execute("""
                SELECT *
                FROM lobby_points_rules_default
                LIMIT 1
            """)
            points = cursor.fetchone()
    
    pre_home = game['pre_home']
    pre_uit = game['pre_uit']
    echt_home = game['echt_home']
    echt_uit = game['echt_uit']
    scores = {'total' : 0}


    ## perfect score
    
    if (pre_home == echt_home and pre_uit == echt_uit):
        scores['perfect_score'] = points['perfect_score']
        scores['total'] = scores['total'] + points['perfect_score']

    ## correct winner

    if ((echt_home < echt_uit and pre_home < pre_uit) or (echt_home > echt_uit and pre_home > pre_uit)):
        scores['correct_winner'] = points['correct_winner']
        scores['total'] = scores['total'] + points['correct_winner']

    ## correct_draw

    if ((echt_home == echt_uit) and (pre_uit == pre_home)):
        scores['correct_draw'] = points['correct_draw']
        scores['total'] = scores['total'] + points['correct_draw']

    ## exact_team_score
    
    if ((echt_home == pre_home) or (echt_uit == pre_uit)):
        scores['exact_team_score'] = points['exact_team_score']
        scores['total'] = scores['total'] + points['exact_team_score']

    ## correct_score_difference

    if ((echt_home - echt_uit) == (pre_home - pre_uit)):
        scores['correct_score_difference'] = points['correct_score_difference']
        scores['total'] = scores['total'] + points['correct_score_difference']

    ## exact_total_score

    if ((echt_home + echt_uit) == (pre_home + pre_uit)):
            scores['exact_total_score'] = points['exact_total_score']
            scores['total'] = scores['total'] + points['exact_total_score']
    print(scores)
    print(points)
    return scores


def get_lobby_leaderboard(lobbyId='', lobbyCode='', cursor=None):
    if not cursor:
        return (
            'Cursor not defined, server error, please contact an admin, (get_lobby_leaderboard)',
            'error',
            500
        )

    if lobbyId == '' and lobbyCode == '':
        return (
            'Lobby ID or lobby code not defined',
            'error',
            400
        )
    if lobbyCode and lobbyId:
         cursor.execute('SELECT COUNT(*) AS aantal_lobbies FROM lobbies WHERE id = %s or code = %s', (lobbyId, lobbyCode))
         lobbies = cursor.fetchone()
         if lobbies['aantal_lobbies'] != 1:
            return (
                'The lobby ID and lobby code do not belong to the same lobby',
                'error',
                400
            )
    cursor.execute(
        """
        SELECT
            users.username,

            COALESCE(bonus.bonus_points, 0) AS bonus_points,

            COALESCE(
                SUM(
                    CASE
                        WHEN rounds.tournamentId = lobbies.tournamentId
                        THEN predictions.points
                        ELSE 0
                    END
                ),
                0
            ) AS points,

            COALESCE(bonus.bonus_points, 0)
            +
            COALESCE(
                SUM(
                    CASE
                        WHEN rounds.tournamentId = lobbies.tournamentId
                        THEN predictions.points
                        ELSE 0
                    END
                ),
                0
            ) AS totaal_points

        FROM lobby_members

        JOIN users
            ON users.id = lobby_members.userId

        JOIN lobbies
            ON lobbies.id = lobby_members.lobbyId

        LEFT JOIN predictions
            ON predictions.userId = users.id

        LEFT JOIN games
            ON games.id = predictions.gameId

        LEFT JOIN rounds
            ON rounds.id = games.roundId

        LEFT JOIN (
            SELECT
                userId,
                lobbyId,
                SUM(points) AS bonus_points
            FROM lobby_bonus_points
            GROUP BY userId, lobbyId
        ) AS bonus
            ON bonus.userId = users.id
            AND bonus.lobbyId = lobbies.id

        WHERE lobbies.id = %s OR lobbies.code = %s

        GROUP BY
            users.id,
            users.username,
            bonus.bonus_points

        ORDER BY totaal_points DESC;
        """,
        (lobbyId, lobbyCode)
    )

    leaderboard = cursor.fetchall()

    return leaderboard, 'success', 200