const lobbyCode = window.location.pathname.split('/').pop();
const api_url = '/api/lobby/code/' + lobbyCode + '/leaderboard';

const response = await fetch(api_url);
const data = await response.json();

data.array.forEach(player => {
    console.log(player)
});