from flask import request, jsonify, flash
from auth.decorators import login_required
from . import api
from db.connection import get_db_connection
from services.lobbies import get_lobby_leaderboard

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

        # ==========================================
        # LOBBY + PUNTENREGELS
        # ==========================================

        cursor.execute("""
            SELECT
                l.id AS lobby_id,
                l.tournamentId,

                lpr.perfect_score,
                lpr.correct_winner,
                lpr.correct_draw,
                lpr.exact_team_score,
                lpr.correct_score_difference,
                lpr.exact_total_score

            FROM lobbies l

            LEFT JOIN lobby_points_rules lpr
                ON lpr.lobbyId = l.id

            WHERE l.code = %s
        """, (lobbyCode,))

        rules = cursor.fetchone()

        if not rules:
            return jsonify({
                "error": "Lobby not found"
            }), 404


        # ==========================================
        # ALLE GAMES VAN HET TOERNOOI
        # ==========================================

        cursor.execute("""
            SELECT
                g.id AS game_id,
                g.status

            FROM games g

            JOIN rounds r
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
            # HAAL DE 2 TEAMS OP
            # ======================================

            cursor.execute("""
                SELECT
                    gt.id AS game_team_id,
                    gt.teamId AS team_id,
                    t.name AS team_name

                FROM game_teams gt

                JOIN teams t
                    ON t.id = gt.teamId

                WHERE gt.gameId = %s

                ORDER BY gt.id ASC
            """, (gameId,))

            teams = cursor.fetchall()


            # Game heeft geen 2 teams
            if len(teams) != 2:
                continue


            team1 = teams[0]
            team2 = teams[1]


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

                actualScores[score["teamId"]] = (
                    score["score"]
                )


            actual1 = actualScores.get(
                team1["team_id"]
            )

            actual2 = actualScores.get(
                team2["team_id"]
            )


            # ======================================
            # GAME OBJECT MAKEN
            # ======================================

            evaluationData[str(gameId)] = {

                "teams": {

                    "team1": team1["team_name"],
                    "team2": team2["team_name"]

                },

                "actual_score": None,

                "players": []
            }


            # ======================================
            # ACTUAL SCORE
            # ======================================

            if (
                actual1 is not None
                and actual2 is not None
            ):

                evaluationData[str(gameId)][
                    "actual_score"
                ] = f"{actual1} - {actual2}"


            # ======================================
            # HAAL ALLE VOORSPELLINGEN OP
            # ======================================

            cursor.execute("""
                SELECT
                    u.username,

                    p.id AS prediction_id,

                    ps.teamId,
                    ps.score AS predicted_score

                FROM lobby_members lm

                JOIN users u
                    ON u.id = lm.userId

                JOIN predictions p
                    ON p.userId = u.id
                    AND p.gameId = %s

                JOIN predicted_scores ps
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
            # GROEPEREN PER GEBRUIKER
            # ======================================

            players = {}


            for prediction in predictionRows:

                username = prediction["username"]

                if username not in players:

                    players[username] = {}


                players[username][
                    prediction["teamId"]
                ] = prediction["predicted_score"]


            # ======================================
            # ELKE SPELER BEREKENEN
            # ======================================

            for username, predictions in players.items():

                predicted1 = predictions.get(
                    team1["team_id"]
                )

                predicted2 = predictions.get(
                    team2["team_id"]
                )


                # Als niet beide voorspellingen bestaan
                if (
                    predicted1 is None
                    or predicted2 is None
                ):
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
                # ALLEEN BEREKENEN ALS SCORES BESTAAN
                # ==================================

                if (
                    actual1 is not None
                    and actual2 is not None
                ):

                    # ------------------------------
                    # PERFECT SCORE
                    # ------------------------------

                    if (
                        predicted1 == actual1
                        and predicted2 == actual2
                    ):

                        perfectScorePoints = (
                            rules["perfect_score"]
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
                            rules["correct_winner"]
                        )

                    elif (
                        predictedDifference < 0
                        and actualDifference < 0
                    ):

                        correctWinnerPoints = (
                            rules["correct_winner"]
                        )


                    # ------------------------------
                    # CORRECT DRAW
                    # ------------------------------

                    if (
                        predictedDifference == 0
                        and actualDifference == 0
                    ):

                        correctDrawPoints = (
                            rules["correct_draw"]
                        )


                    # ------------------------------
                    # EXACT TEAM SCORE
                    # ------------------------------

                    if predicted1 == actual1:

                        exactTeamScorePoints += (
                            rules["exact_team_score"]
                        )


                    if predicted2 == actual2:

                        exactTeamScorePoints += (
                            rules["exact_team_score"]
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
                            rules[
                                "correct_score_difference"
                            ]
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
                            rules["exact_total_score"]
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

                evaluationData[
                    str(gameId)
                ]["players"].append({

                    "username": username,

                    "prediction_score":
                        f"{predicted1} - {predicted2}",

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


        return jsonify(evaluationData)


    finally:

        cursor.close()
        db.close()

@api.route('/lobby/code/<code>/leaderboard')
@api.route('/lobby/id/<int:id>/leaderboard')
def api_get_lobby_leaderboard(code=None, id=None):
    db, cursor = get_db_connection()
    
    leaderboard, status, error_code = get_lobby_leaderboard(lobbyId=id, lobbyCode=code, cursor=cursor)
    print(code)

    cursor.close()
    db.close()

    if status == 'error':
        error_msg = leaderboard
        flash(error_msg, 'error')
        return error_msg, error_code

    
    return leaderboard, 200