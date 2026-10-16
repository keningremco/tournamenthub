
const publicTournamentCode = document.getElementById("publicTournamentCode");
const findPublicLobbiesButton = document.getElementById("findPublicLobbies");
const publicLobbyResults = document.getElementById("publicLobbyResults");

function showPublicLobbyMessage(message) {
    if (!publicLobbyResults) return;

    publicLobbyResults.replaceChildren();

    const resultMessage = document.createElement("div");
    resultMessage.className = "result-message";
    resultMessage.textContent = message;

    publicLobbyResults.appendChild(resultMessage);
}

function createPublicLobbyResult(lobby) {
    const result = document.createElement("div");
    result.className = "public-lobby-result";

    const lobbyInformation = document.createElement("div");

    const lobbyName = document.createElement("div");
    lobbyName.className = "public-lobby-name";
    lobbyName.textContent = lobby.name;

    const lobbyMeta = document.createElement("div");
    lobbyMeta.className = "public-lobby-meta";
    lobbyMeta.textContent =
        `${lobby.tournament_name} · ${lobby.member_count} player(s)`;

    lobbyInformation.append(lobbyName, lobbyMeta);

    const joinForm = document.createElement("form");
    joinForm.action = "/joinlobby";
    joinForm.method = "post";

    const codeInput = document.createElement("input");
    codeInput.type = "hidden";
    codeInput.name = "code";
    codeInput.value = lobby.code;

    const joinButton = document.createElement("button");
    joinButton.type = "submit";
    joinButton.textContent = "Join lobby";

    joinForm.append(codeInput, joinButton);
    result.append(lobbyInformation, joinForm);

    return result;
}

async function findPublicLobbies() {
    if (!publicTournamentCode || !findPublicLobbiesButton || !publicLobbyResults) {
        return;
    }

    const tournamentCode = publicTournamentCode.value.trim().toUpperCase();

    if (!tournamentCode) {
        showPublicLobbyMessage("Enter a tournament code first.");
        return;
    }

    findPublicLobbiesButton.disabled = true;
    findPublicLobbiesButton.textContent = "Searching...";

    try {
        const response = await fetch(
            `/api/lobbies/public?tournament_code=${encodeURIComponent(tournamentCode)}`
        );

        if (!response.ok) {
            throw new Error("Could not load public lobbies.");
        }

        const lobbies = await response.json();

        publicLobbyResults.replaceChildren();

        if (!lobbies.length) {
            showPublicLobbyMessage(
                "No public lobbies were found for this tournament."
            );
            return;
        }

        lobbies.forEach(lobby => {
            publicLobbyResults.appendChild(createPublicLobbyResult(lobby));
        });
    } catch (error) {
        showPublicLobbyMessage(
            "Something went wrong while searching for public lobbies."
        );
    } finally {
        findPublicLobbiesButton.disabled = false;
        findPublicLobbiesButton.textContent = "Find lobbies";
    }
}

if (findPublicLobbiesButton) {
    findPublicLobbiesButton.addEventListener("click", findPublicLobbies);
}

if (publicTournamentCode) {
    publicTournamentCode.addEventListener("keydown", event => {
        if (event.key === "Enter") {
            event.preventDefault();
            findPublicLobbies();
        }
    });

    if (publicTournamentCode.value.trim()) {
        findPublicLobbies();
    }
}
