from db.connection import get_db_connection

def get_permissions(userId, tournamentId=None, lobbyId=None, site=False):
    db, cursor = get_db_connection()

    permissions = {
        "site": [],
        "tournaments": {},
        "lobbies": {}
    }

    # Als er geen specifieke tournament/lobby is opgegeven,
    # haal alle tournaments en lobbies op.
    get_all = tournamentId is None and lobbyId is None

    # -------------------------
    # SITE
    # -------------------------
    if site:
        cursor.execute("""
            SELECT permissions.name
            FROM user_roles
            JOIN roles
                ON user_roles.roleId = roles.id
            JOIN role_permissions
                ON roles.id = role_permissions.roleId
            JOIN permissions
                ON role_permissions.permissionId = permissions.Id
            WHERE user_roles.userId = %s
              AND user_roles.scopeType = 'site'
        """, (userId,))

        permissions["site"] = [
            row["name"] for row in cursor.fetchall()
        ]

    # -------------------------
    # TOURNAMENTS
    # -------------------------
    if tournamentId is not None:
        # Alleen deze tournament
        cursor.execute("""
            SELECT permissions.name
            FROM user_roles
            JOIN roles
                ON user_roles.roleId = roles.id
            JOIN role_permissions
                ON roles.id = role_permissions.roleId
            JOIN permissions
                ON role_permissions.permissionId = permissions.Id
            WHERE user_roles.userId = %s
              AND user_roles.scopeType = 'tournament'
              AND user_roles.scopeId = %s
        """, (userId, tournamentId))

        permissions["tournaments"][str(tournamentId)] = [
            row["name"] for row in cursor.fetchall()
        ]

    elif get_all:
        # Alle tournaments van deze user
        cursor.execute("""
            SELECT
                user_roles.scopeId AS tournamentId,
                permissions.name
            FROM user_roles
            JOIN roles
                ON user_roles.roleId = roles.id
            JOIN role_permissions
                ON roles.id = role_permissions.roleId
            JOIN permissions
                ON role_permissions.permissionId = permissions.Id
            WHERE user_roles.userId = %s
              AND user_roles.scopeType = 'tournament'
        """, (userId,))

        for row in cursor.fetchall():
            tournament_id = str(row["tournamentId"])

            if tournament_id not in permissions["tournaments"]:
                permissions["tournaments"][tournament_id] = []

            permissions["tournaments"][tournament_id].append(
                row["name"]
            )

    # -------------------------
    # LOBBIES
    # -------------------------
    if lobbyId is not None:
        # Alleen deze lobby
        cursor.execute("""
            SELECT permissions.name
            FROM user_roles
            JOIN roles
                ON user_roles.roleId = roles.id
            JOIN role_permissions
                ON roles.id = role_permissions.roleId
            JOIN permissions
                ON role_permissions.permissionId = permissions.Id
            WHERE user_roles.userId = %s
              AND user_roles.scopeType = 'lobby'
              AND user_roles.scopeId = %s
        """, (userId, lobbyId))

        permissions["lobbies"][str(lobbyId)] = [
            row["name"] for row in cursor.fetchall()
        ]

    elif get_all:
        # Alle lobbies van deze user
        cursor.execute("""
            SELECT
                user_roles.scopeId AS lobbyId,
                permissions.name
            FROM user_roles
            JOIN roles
                ON user_roles.roleId = roles.id
            JOIN role_permissions
                ON roles.id = role_permissions.roleId
            JOIN permissions
                ON role_permissions.permissionId = permissions.Id
            WHERE user_roles.userId = %s
              AND user_roles.scopeType = 'lobby'
        """, (userId,))

        for row in cursor.fetchall():
            lobby_id = str(row["lobbyId"])

            if lobby_id not in permissions["lobbies"]:
                permissions["lobbies"][lobby_id] = []

            permissions["lobbies"][lobby_id].append(
                row["name"]
            )

    cursor.close()
    db.close()

    return permissions

def can_user(userId, permission=None, tournamentId=None, lobbyId=None, site=True):

    permissions = get_permissions(userId, tournamentId, lobbyId, site)
    if permission is None:
        return permissions
    
    if tournamentId is not None:
        return permission in permissions["tournaments"].get(
            str(tournamentId), []
        )
    if lobbyId is not None:
        return permission in permissions["lobbies"].get(
            str(lobbyId), []
        )
    return permission in permissions["site"]