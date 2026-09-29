const lobbyCode = window.location.pathname.split('/').pop();
const api_url = '/api/lobby/code/' + lobbyCode + '/leaderboard';
const leaderboard = document.getElementById('scoreboard')


function drawPlayer(player, index) {
    leaderboard.innerHTML += `
    <div class="scoreboard-player">

        <div class="rank">
            ${index + 1}
        </div>


        <div class="player-name">
            ${ player.username }
        </div>


        <div class="player-points normal-points">
            ${ player.points } pts
        </div>

        <div class="player-points bonus-points">
            +${ player.bonus_points } bonus pts
        </div>

        <div class="player-points total-points">
            = ${ player.totaal_points } totaal pts
        </div>

        <div class="player-points compact-points">
            ${ player.points } + ${ player.bonus_points } = ${ player.totaal_points }
        </div>
    </div>
    `;

}

async function resetLeaderboard() {
    leaderboard.innerHTML = '';
    const response = await fetch(api_url);
    const data = await response.json();

    data.forEach((player, index) => {
        drawPlayer(player, index);
        
    });
}

resetLeaderboard();
