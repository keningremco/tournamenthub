
document.addEventListener("DOMContentLoaded", function () {

    const buttons = document.querySelectorAll(".evaluation-toggle");

    buttons.forEach(function (button) {

        button.addEventListener("click", function () {

            const gameId = this.dataset.gameId;

            const dropdown = document.getElementById(
                `evaluation-dropdown-${gameId}`
            );

            const dataElement = document.getElementById(
                `evaluation-data-${gameId}`
            );

            if (!dropdown || !dataElement) {
                return;
            }


            /* =====================================
               OPEN / CLOSE
               ===================================== */

            if (dropdown.classList.contains("open")) {

                dropdown.classList.remove("open");
                dropdown.innerHTML = "";

                return;
            }


            /* =====================================
               JSON INLEZEN
               ===================================== */

            let evaluations;

            try {
                evaluations = JSON.parse(
                    dataElement.textContent
                );
            } catch (error) {

                console.error(
                    "Could not parse evaluation data:",
                    error
                );

                dropdown.innerHTML = `
                    <div class="evaluation-error">
                        Could not load predictions.
                    </div>
                `;

                dropdown.classList.add("open");

                return;
            }


            const players = evaluations.players || [];


            /* =====================================
               HUIDIGE USER
               ===================================== */

            const predictionBox = document.querySelector(
                `.prediction-box[data-game-id="${gameId}"]`
            );

            const currentUserId = predictionBox
                ? String(predictionBox.dataset.userId)
                : null;


            /* =====================================
               CONTAINER
               ===================================== */

            const container = document.createElement("div");

            container.className = "evaluation-list";


            /* =====================================
               ACTUAL SCORE
               ===================================== */

            if (evaluations.actual_score) {

                const actual = document.createElement("div");

                actual.className = "evaluation-actual";

                actual.innerHTML = `
                    <span class="evaluation-actual-label">
                        Actual score
                    </span>

                    <strong>
                        ${escapeHtml(evaluations.actual_score)}
                    </strong>
                `;

                container.appendChild(actual);
            }


            /* =====================================
               PLAYERS
               ===================================== */

            if (players.length === 0) {

                container.insertAdjacentHTML(
                    "beforeend",
                    `
                    <div class="evaluation-empty">
                        No predictions found.
                    </div>
                    `
                );

            } else {

                players.forEach(function (player) {

                    const row = document.createElement("div");

                    row.className = "evaluation-player";


                    /* Eigen speler herkennen */

                    if (
                        currentUserId !== null &&
                        player.userId !== undefined &&
                        String(player.userId) === currentUserId
                    ) {
                        row.classList.add("current-player");
                    }


                    const username = escapeHtml(
                        player.username ?? ""
                    );


                    const prediction =
                        player.prediction_score ??
                        `${player.predictedscorehome ?? "-"} - ${player.predictedscoreuit ?? "-"}`;


                    const total =
                        player.total ?? 0;


                    row.innerHTML = `

                        <div class="evaluation-player-main">

                            <div class="evaluation-player-name">

                                ${username}

                                ${
                                    currentUserId !== null &&
                                    player.userId !== undefined &&
                                    String(player.userId) === currentUserId
                                    ? '<span class="you-label">You</span>'
                                    : ''
                                }

                            </div>


                            <div class="evaluation-player-score">
                                ${escapeHtml(String(prediction))}
                            </div>

                        </div>


                        <div class="evaluation-player-points">
                            ${escapeHtml(String(total))} pts
                        </div>


                        <div class="evaluation-breakdown">

                            <span>
                                Perfect:
                                ${player.perfect_score ?? 0}
                            </span>

                            <span>
                                Winner:
                                ${player.correct_winner ?? 0}
                            </span>

                            <span>
                                Draw:
                                ${player.correct_draw ?? 0}
                            </span>

                            <span>
                                Exact team:
                                ${player.exact_team_score ?? 0}
                            </span>

                            <span>
                                Difference:
                                ${player.correct_score_difference ?? 0}
                            </span>

                            <span>
                                Total:
                                ${player.exact_total_score ?? 0}
                            </span>

                        </div>
                    `;

                    container.appendChild(row);
                });
            }


            dropdown.innerHTML = "";
            dropdown.appendChild(container);

            dropdown.classList.add("open");

        });

    });


    /* =========================================
       HTML ESCAPEN
       ========================================= */

    function escapeHtml(value) {

        const div = document.createElement("div");

        div.textContent = value;

        return div.innerHTML;
    }

});
