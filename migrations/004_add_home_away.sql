ALTER TABLE `game_teams` ADD `home_away` ENUM('home','away') NOT NULL AFTER `teamId`;

UPDATE game_teams gt
JOIN (
    SELECT gameId, MAX(id) AS away_id
    FROM game_teams
    GROUP BY gameId
) latest
    ON latest.gameId = gt.gameId
   AND latest.away_id = gt.id
SET gt.home_away = 'away';