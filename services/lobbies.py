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

def get_evals(cursor, lobbyCode):
    # ==========================================
    # LOBBY + PUNTENREGELS
    # ==========================================

    cursor.execute("""
        SELECT
            l.id AS lobby_id,
            l.tournamentId,

            COALESCE(
                lpr.perfect_score,
                (SELECT perfect_score
                 FROM lobby_points_rules_default
                 LIMIT 1)
            ) AS perfect_score,

            COALESCE(
                lpr.correct_winner,
                (SELECT correct_winner
                 FROM lobby_points_rules_default
                 LIMIT 1)
            ) AS correct_winner,

            COALESCE(
                lpr.correct_draw,
                (SELECT correct_draw
                 FROM lobby_points_rules_default
                 LIMIT 1)
            ) AS correct_draw,

            COALESCE(
                lpr.exact_team_score,
                (SELECT exact_team_score
                 FROM lobby_points_rules_default
                 LIMIT 1)
            ) AS exact_team_score,

            COALESCE(
                lpr.correct_score_difference,
                (SELECT correct_score_difference
                 FROM lobby_points_rules_default
                 LIMIT 1)
            ) AS correct_score_difference,

            COALESCE(
                lpr.exact_total_score,
                (SELECT exact_total_score
                 FROM lobby_points_rules_default
                 LIMIT 1)
            ) AS exact_total_score

        FROM lobbies l

        LEFT JOIN lobby_points_rules lpr
            ON lpr.lobbyId = l.id

        WHERE l.code = %s
    """, (lobbyCode,))

    rules = cursor.fetchone()

    if not rules:
        return 'error', 404


    # ==========================================
    # ALLE GAMES VAN HET TOERNOOI
    # ==========================================

    cursor.execute("""
        SELECT
            g.id AS game_id,
            g.status

        FROM games g

        INNER JOIN rounds r
            ON r.id = g.roundId

        WHERE r.tournamentId = %s

        ORDER BY g.id
    """, (rules["tournamentId"],))

    gameRows = cursor.fetchall()


    # ==========================================
    # FINALE DATA
    # ==========================================

    evaluationData = {}


    # ==========================================
    # LOOP DOOR ELKE GAME
    # ==========================================

    for game in gameRows:

        gameId = game["game_id"]


        # ======================================
        # HAAL GAME TEAMS OP
        # LEFT JOIN ZODAT EEN GAME NIET
        # VERDWIJNT ALS DE TEAM-ROW ONTBREEKT
        # ======================================

        cursor.execute("""
            SELECT
                gt.id AS game_team_id,
                gt.teamId AS team_id,
                t.name AS team_name

            FROM game_teams gt

            LEFT JOIN teams t
                ON t.id = gt.teamId

            WHERE gt.gameId = %s

            ORDER BY gt.id ASC
        """, (gameId,))

        teams = cursor.fetchall()


        # ======================================
        # GAME OBJECT ALTIJD AANMAKEN
        #
        # BELANGRIJK:
        # Vroeger deed je:
        #
        # if len(teams) != 2:
        #     continue
        #
        # Daardoor verdween de hele game uit
        # de response.
        # ======================================

        team1 = teams[0] if len(teams) >= 1 else None
        team2 = teams[1] if len(teams) >= 2 else None


        evaluationData[gameId] = {
            "teams": {
                "team1": team1["team_name"] if team1 else None,
                "team2": team2["team_name"] if team2 else None
            },

            "actual_score": None,

            "players": []
        }


        # ======================================
        # ZONDER 2 TEAMS KUN JE GEEN
        # PREDICTION/EVALUATIE BEREKENEN
        #
        # MAAR DE GAME BLIJFT WEL IN DATA
        # ======================================

        if team1 is None or team2 is None:
            continue


        # ======================================
        # HAAL DE ECHTE SCORES OP
        # ======================================

        cursor.execute("""
            SELECT
                teamId,
                score

            FROM scores

            WHERE gameId = %s
        """, (gameId,))

        scoreRows = cursor.fetchall()


        actualScores = {}

        for score in scoreRows:
            actualScores[score["teamId"]] = score["score"]


        actual1 = actualScores.get(team1["team_id"])
        actual2 = actualScores.get(team2["team_id"])


        # ======================================
        # ACTUAL SCORE
        # ======================================

        if actual1 is not None and actual2 is not None:
            evaluationData[gameId]["actual_score"] = (
                f"{actual1} - {actual2}"
            )


        # ======================================
        # ALLE LOBBY MEMBERS + PREDICTIONS
        #
        # LEFT JOIN BEHOUDT OOK USERS ZONDER
        # PREDICTION.
        # ======================================

        cursor.execute("""
            SELECT
                lm.userId AS user_id,
                u.username,

                p.id AS prediction_id,

                ps.teamId,
                ps.score AS predicted_score

            FROM lobby_members lm

            LEFT JOIN users u
                ON u.id = lm.userId

            LEFT JOIN predictions p
                ON p.userId = lm.userId
                AND p.gameId = %s

            LEFT JOIN predicted_scores ps
                ON ps.predictionId = p.id

            WHERE lm.lobbyId = %s

            ORDER BY
                u.username,
                ps.teamId
        """, (
            gameId,
            rules["lobby_id"]
        ))

        predictionRows = cursor.fetchall()


        # ======================================
        # GROEPEREN PER USER
        # ======================================

        players = {}

        for prediction in predictionRows:

            userId = prediction["user_id"]
            username = prediction["username"]

            if userId not in players:
                players[userId] = {
                    "username": username,
                    "predictions": {}
                }


            # LEFT JOIN KAN NULL OPLEVEREN
            # ALS ER GEEN PREDICTION BESTAAT.
            if prediction["teamId"] is not None:

                players[userId]["predictions"][
                    prediction["teamId"]
                ] = prediction["predicted_score"]


        # ======================================
        # ELKE SPELER BEREKENEN
        # ======================================

        for userId, playerData in players.items():

            username = playerData["username"]
            predictions = playerData["predictions"]


            predicted1 = predictions.get(
                team1["team_id"]
            )

            predicted2 = predictions.get(
                team2["team_id"]
            )


            # ==================================
            # ALS NIET BEIDE VOORSPELLINGEN
            # BESTAAN:
            #
            # ZELFDE GEDRAG ALS JE OUDE CODE:
            # NIET BEREKENEN / NIET TOEVOEGEN.
            # ==================================

            if predicted1 is None or predicted2 is None:
                continue


            # ==================================
            # START PUNTEN
            # ==================================

            perfectScorePoints = 0
            correctWinnerPoints = 0
            correctDrawPoints = 0
            exactTeamScorePoints = 0
            correctScoreDifferencePoints = 0
            exactTotalScorePoints = 0


            # ==================================
            # ALLEEN BEREKENEN ALS ECHTE SCORES
            # BESTAAN
            # ==================================

            if actual1 is not None and actual2 is not None:

                # ------------------------------
                # PERFECT SCORE
                # ------------------------------

                if (
                    predicted1 == actual1
                    and predicted2 == actual2
                ):
                    perfectScorePoints = (
                        rules["perfect_score"] or 0
                    )


                # ------------------------------
                # SCORE DIFFERENCE
                # ------------------------------

                predictedDifference = (
                    predicted1 - predicted2
                )

                actualDifference = (
                    actual1 - actual2
                )


                # ------------------------------
                # CORRECT WINNER
                # ------------------------------

                if (
                    predictedDifference > 0
                    and actualDifference > 0
                ):
                    correctWinnerPoints = (
                        rules["correct_winner"] or 0
                    )

                elif (
                    predictedDifference < 0
                    and actualDifference < 0
                ):
                    correctWinnerPoints = (
                        rules["correct_winner"] or 0
                    )


                # ------------------------------
                # CORRECT DRAW
                # ------------------------------

                if (
                    predictedDifference == 0
                    and actualDifference == 0
                ):
                    correctDrawPoints = (
                        rules["correct_draw"] or 0
                    )


                # ------------------------------
                # EXACT TEAM SCORE
                # ------------------------------

                if predicted1 == actual1:
                    exactTeamScorePoints += (
                        rules["exact_team_score"] or 0
                    )

                if predicted2 == actual2:
                    exactTeamScorePoints += (
                        rules["exact_team_score"] or 0
                    )


                # ------------------------------
                # CORRECT SCORE DIFFERENCE
                # ------------------------------

                if (
                    predictedDifference
                    ==
                    actualDifference
                ):
                    correctScoreDifferencePoints = (
                        rules["correct_score_difference"] or 0
                    )


                # ------------------------------
                # EXACT TOTAL SCORE
                # ------------------------------

                if (
                    predicted1 + predicted2
                    ==
                    actual1 + actual2
                ):
                    exactTotalScorePoints = (
                        rules["exact_total_score"] or 0
                    )


            # ==================================
            # TOTAL
            # ==================================

            total = (
                perfectScorePoints
                + correctWinnerPoints
                + correctDrawPoints
                + exactTeamScorePoints
                + correctScoreDifferencePoints
                + exactTotalScorePoints
            )


            # ==================================
            # SPELER TOEVOEGEN
            # ==================================

            evaluationData[gameId]["players"].append({

                "username": username,

                "userId" : userId,
                
                "prediction_score":
                    f"{predicted1} - {predicted2}",

                "predictedscorehome":
                    predicted1,

                "predictedscoreuit":
                    predicted2,

                "perfect_score":
                    perfectScorePoints,

                "correct_winner":
                    correctWinnerPoints,

                "correct_draw":
                    correctDrawPoints,

                "exact_team_score":
                    exactTeamScorePoints,

                "correct_score_difference":
                    correctScoreDifferencePoints,

                "exact_total_score":
                    exactTotalScorePoints,

                "total":
                    total
            })


    return evaluationData