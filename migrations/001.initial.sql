-- phpMyAdmin SQL Dump
-- version 5.2.2deb1+deb13u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Gegenereerd op: 17 sep 2026 om 17:25
-- Serverversie: 11.8.6-MariaDB-0+deb13u1 from Debian
-- PHP-versie: 8.4.24

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tournamenthub`
--

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `icon` varchar(10) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `email_verification_tokens`
--

CREATE TABLE `email_verification_tokens` (
  `id` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `token` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `featured_tags`
--

CREATE TABLE `featured_tags` (
  `id` int(11) NOT NULL,
  `tagId` int(11) NOT NULL,
  `sortOrder` int(11) NOT NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `games`
--

CREATE TABLE `games` (
  `id` int(11) NOT NULL,
  `start_time` datetime DEFAULT NULL,
  `roundId` int(11) DEFAULT NULL,
  `stadiumId` int(11) DEFAULT NULL,
  `status` enum('scheduled','in_progress','awaiting_scores','completed','cancelled') DEFAULT 'scheduled'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `game_teams`
--

CREATE TABLE `game_teams` (
  `id` int(11) NOT NULL,
  `gameId` int(11) NOT NULL,
  `teamId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `lobbies`
--

CREATE TABLE `lobbies` (
  `id` int(11) NOT NULL,
  `tournamentId` int(11) NOT NULL,
  `makerId` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `code` char(8) NOT NULL,
  `isPrivate` tinyint(1) NOT NULL DEFAULT 0,
  `password` varchar(100) DEFAULT NULL,
  `isLocked` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `lobby_bonus_points`
--

CREATE TABLE `lobby_bonus_points` (
  `userId` int(11) NOT NULL,
  `lobbyId` int(11) NOT NULL,
  `points` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `lobby_members`
--

CREATE TABLE `lobby_members` (
  `lobbyId` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `joined_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `lobby_points_rules`
--

CREATE TABLE `lobby_points_rules` (
  `id` int(11) NOT NULL,
  `lobbyId` int(11) NOT NULL,
  `perfect_score` int(11) NOT NULL DEFAULT 10,
  `correct_winner` int(11) NOT NULL DEFAULT 5,
  `correct_draw` int(11) NOT NULL DEFAULT 5,
  `exact_team_score` int(11) NOT NULL DEFAULT 2,
  `correct_score_difference` int(11) NOT NULL DEFAULT 3,
  `exact_total_score` int(11) NOT NULL DEFAULT 3
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `permissions`
--

CREATE TABLE `permissions` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `predicted_scores`
--

CREATE TABLE `predicted_scores` (
  `id` int(11) NOT NULL,
  `predictionId` int(11) NOT NULL,
  `teamId` int(11) NOT NULL,
  `score` int(11) NOT NULL DEFAULT 0,
  `points` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `predictions`
--

CREATE TABLE `predictions` (
  `id` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `gameId` int(11) NOT NULL,
  `points` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `referee_games`
--

CREATE TABLE `referee_games` (
  `id` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `gameId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `role_permissions`
--

CREATE TABLE `role_permissions` (
  `id` int(11) NOT NULL,
  `roleId` int(11) NOT NULL,
  `permissionId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `rounds`
--

CREATE TABLE `rounds` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `tournamentId` int(11) NOT NULL,
  `roundNumber` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `scores`
--

CREATE TABLE `scores` (
  `id` int(11) NOT NULL,
  `gameId` int(11) NOT NULL,
  `teamId` int(11) NOT NULL,
  `score` int(11) DEFAULT NULL,
  `result` enum('won','lost','draw') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `stadiums`
--

CREATE TABLE `stadiums` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `tournamentId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `stadium_teams`
--

CREATE TABLE `stadium_teams` (
  `id` int(11) NOT NULL,
  `stadiumId` int(11) NOT NULL,
  `teamId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `tags`
--

CREATE TABLE `tags` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `verified` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `teams`
--

CREATE TABLE `teams` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `official` tinyint(1) DEFAULT 0,
  `tournamentId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `tournaments`
--

CREATE TABLE `tournaments` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `visibility` enum('public','private','unlisted') NOT NULL DEFAULT 'private',
  `status` enum('draft','registration_open','registration_closed','scheduled','ongoing','paused','completed','cancelled','archived') DEFAULT 'draft',
  `verified` tinyint(1) NOT NULL DEFAULT 0,
  `verifiedBy` int(11) DEFAULT NULL,
  `code` char(8) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `tournament_tags`
--

CREATE TABLE `tournament_tags` (
  `tournamentId` int(11) NOT NULL,
  `tagId` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `email` varchar(255) DEFAULT NULL,
  `email_verified` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

-- --------------------------------------------------------

--
-- Tabelstructuur voor tabel `user_roles`
--

CREATE TABLE `user_roles` (
  `id` int(11) NOT NULL,
  `userId` int(11) NOT NULL,
  `roleId` int(11) NOT NULL,
  `scopeType` enum('site','tournament','lobby') NOT NULL,
  `scopeId` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Indexen voor geëxporteerde tabellen
--

--
-- Indexen voor tabel `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexen voor tabel `email_verification_tokens`
--
ALTER TABLE `email_verification_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `userId` (`userId`);

--
-- Indexen voor tabel `featured_tags`
--
ALTER TABLE `featured_tags`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tagId` (`tagId`);

--
-- Indexen voor tabel `games`
--
ALTER TABLE `games`
  ADD PRIMARY KEY (`id`),
  ADD KEY `roundId` (`roundId`),
  ADD KEY `fk_games_stadium` (`stadiumId`);

--
-- Indexen voor tabel `game_teams`
--
ALTER TABLE `game_teams`
  ADD PRIMARY KEY (`id`),
  ADD KEY `gameId` (`gameId`),
  ADD KEY `teamId` (`teamId`);

--
-- Indexen voor tabel `lobbies`
--
ALTER TABLE `lobbies`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `tournamentId` (`tournamentId`),
  ADD KEY `makerId` (`makerId`);

--
-- Indexen voor tabel `lobby_bonus_points`
--
ALTER TABLE `lobby_bonus_points`
  ADD PRIMARY KEY (`userId`,`lobbyId`),
  ADD KEY `fk_lobby_bonus_points_lobby` (`lobbyId`);

--
-- Indexen voor tabel `lobby_members`
--
ALTER TABLE `lobby_members`
  ADD PRIMARY KEY (`lobbyId`,`userId`),
  ADD KEY `userId` (`userId`);

--
-- Indexen voor tabel `lobby_points_rules`
--
ALTER TABLE `lobby_points_rules`
  ADD PRIMARY KEY (`id`),
  ADD KEY `lobbyId` (`lobbyId`);

--
-- Indexen voor tabel `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_permissions_name` (`name`);

--
-- Indexen voor tabel `predicted_scores`
--
ALTER TABLE `predicted_scores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_prediction_team` (`predictionId`,`teamId`),
  ADD KEY `fk_predicted_scores_team` (`teamId`);

--
-- Indexen voor tabel `predictions`
--
ALTER TABLE `predictions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_prediction` (`userId`,`gameId`),
  ADD KEY `fk_predictions_game` (`gameId`);

--
-- Indexen voor tabel `referee_games`
--
ALTER TABLE `referee_games`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_referee_game` (`userId`,`gameId`),
  ADD KEY `idx_referee_games_user` (`userId`),
  ADD KEY `idx_referee_games_game` (`gameId`);

--
-- Indexen voor tabel `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_roles_name` (`name`);

--
-- Indexen voor tabel `role_permissions`
--
ALTER TABLE `role_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_role_permission` (`roleId`,`permissionId`),
  ADD KEY `idx_role_permissions_role` (`roleId`),
  ADD KEY `idx_role_permissions_permission` (`permissionId`);

--
-- Indexen voor tabel `rounds`
--
ALTER TABLE `rounds`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tournamentId` (`tournamentId`,`roundNumber`);

--
-- Indexen voor tabel `scores`
--
ALTER TABLE `scores`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_game_team` (`gameId`,`teamId`),
  ADD KEY `fk_scores_team` (`teamId`);

--
-- Indexen voor tabel `stadiums`
--
ALTER TABLE `stadiums`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_stadiums_tournament` (`tournamentId`);

--
-- Indexen voor tabel `stadium_teams`
--
ALTER TABLE `stadium_teams`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uk_stadium_team` (`stadiumId`,`teamId`),
  ADD KEY `fk_stadium_teams_team` (`teamId`);

--
-- Indexen voor tabel `tags`
--
ALTER TABLE `tags`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexen voor tabel `teams`
--
ALTER TABLE `teams`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_teams_tournament` (`tournamentId`);

--
-- Indexen voor tabel `tournaments`
--
ALTER TABLE `tournaments`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `code` (`code`),
  ADD KEY `verifiedBy` (`verifiedBy`);

--
-- Indexen voor tabel `tournament_tags`
--
ALTER TABLE `tournament_tags`
  ADD PRIMARY KEY (`tournamentId`,`tagId`),
  ADD KEY `tagId` (`tagId`);

--
-- Indexen voor tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexen voor tabel `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `uq_user_role_scope` (`userId`,`roleId`,`scopeType`,`scopeId`),
  ADD KEY `idx_user_roles_user` (`userId`),
  ADD KEY `idx_user_roles_role` (`roleId`),
  ADD KEY `idx_user_roles_scope` (`scopeType`,`scopeId`);

--
-- AUTO_INCREMENT voor geëxporteerde tabellen
--

--
-- AUTO_INCREMENT voor een tabel `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `email_verification_tokens`
--
ALTER TABLE `email_verification_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `featured_tags`
--
ALTER TABLE `featured_tags`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `games`
--
ALTER TABLE `games`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `game_teams`
--
ALTER TABLE `game_teams`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `lobbies`
--
ALTER TABLE `lobbies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `lobby_points_rules`
--
ALTER TABLE `lobby_points_rules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `predicted_scores`
--
ALTER TABLE `predicted_scores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `predictions`
--
ALTER TABLE `predictions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `referee_games`
--
ALTER TABLE `referee_games`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `role_permissions`
--
ALTER TABLE `role_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `rounds`
--
ALTER TABLE `rounds`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `scores`
--
ALTER TABLE `scores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `stadiums`
--
ALTER TABLE `stadiums`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `stadium_teams`
--
ALTER TABLE `stadium_teams`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `tags`
--
ALTER TABLE `tags`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `teams`
--
ALTER TABLE `teams`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `tournaments`
--
ALTER TABLE `tournaments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT voor een tabel `user_roles`
--
ALTER TABLE `user_roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Beperkingen voor geëxporteerde tabellen
--

--
-- Beperkingen voor tabel `email_verification_tokens`
--
ALTER TABLE `email_verification_tokens`
  ADD CONSTRAINT `email_verification_tokens_ibfk_1` FOREIGN KEY (`userId`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `featured_tags`
--
ALTER TABLE `featured_tags`
  ADD CONSTRAINT `fk_featured_tags_tag` FOREIGN KEY (`tagId`) REFERENCES `tags` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `games`
--
ALTER TABLE `games`
  ADD CONSTRAINT `fk_games_stadium` FOREIGN KEY (`stadiumId`) REFERENCES `stadiums` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `games_ibfk_1` FOREIGN KEY (`roundId`) REFERENCES `rounds` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `game_teams`
--
ALTER TABLE `game_teams`
  ADD CONSTRAINT `game_teams_ibfk_1` FOREIGN KEY (`gameId`) REFERENCES `games` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `game_teams_ibfk_2` FOREIGN KEY (`teamId`) REFERENCES `teams` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `lobbies`
--
ALTER TABLE `lobbies`
  ADD CONSTRAINT `lobbies_ibfk_1` FOREIGN KEY (`tournamentId`) REFERENCES `tournaments` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lobbies_ibfk_2` FOREIGN KEY (`makerId`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `lobby_bonus_points`
--
ALTER TABLE `lobby_bonus_points`
  ADD CONSTRAINT `fk_lobby_bonus_points_lobby` FOREIGN KEY (`lobbyId`) REFERENCES `lobbies` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_lobby_bonus_points_user` FOREIGN KEY (`userId`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `lobby_members`
--
ALTER TABLE `lobby_members`
  ADD CONSTRAINT `lobby_members_ibfk_1` FOREIGN KEY (`lobbyId`) REFERENCES `lobbies` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `lobby_members_ibfk_2` FOREIGN KEY (`userId`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `lobby_points_rules`
--
ALTER TABLE `lobby_points_rules`
  ADD CONSTRAINT `lobby_points_rules_ibfk_1` FOREIGN KEY (`lobbyId`) REFERENCES `lobbies` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `predicted_scores`
--
ALTER TABLE `predicted_scores`
  ADD CONSTRAINT `fk_predicted_scores_prediction` FOREIGN KEY (`predictionId`) REFERENCES `predictions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_predicted_scores_team` FOREIGN KEY (`teamId`) REFERENCES `teams` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `predictions`
--
ALTER TABLE `predictions`
  ADD CONSTRAINT `fk_predictions_game` FOREIGN KEY (`gameId`) REFERENCES `games` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_predictions_user` FOREIGN KEY (`userId`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `referee_games`
--
ALTER TABLE `referee_games`
  ADD CONSTRAINT `fk_referee_games_game` FOREIGN KEY (`gameId`) REFERENCES `games` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_referee_games_user` FOREIGN KEY (`userId`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `role_permissions`
--
ALTER TABLE `role_permissions`
  ADD CONSTRAINT `fk_role_permissions_permission` FOREIGN KEY (`permissionId`) REFERENCES `permissions` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_role_permissions_role` FOREIGN KEY (`roleId`) REFERENCES `roles` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `rounds`
--
ALTER TABLE `rounds`
  ADD CONSTRAINT `rounds_ibfk_1` FOREIGN KEY (`tournamentId`) REFERENCES `tournaments` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `scores`
--
ALTER TABLE `scores`
  ADD CONSTRAINT `fk_scores_game` FOREIGN KEY (`gameId`) REFERENCES `games` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_scores_team` FOREIGN KEY (`teamId`) REFERENCES `teams` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `stadiums`
--
ALTER TABLE `stadiums`
  ADD CONSTRAINT `fk_stadiums_tournament` FOREIGN KEY (`tournamentId`) REFERENCES `tournaments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Beperkingen voor tabel `stadium_teams`
--
ALTER TABLE `stadium_teams`
  ADD CONSTRAINT `fk_stadium_teams_stadium` FOREIGN KEY (`stadiumId`) REFERENCES `stadiums` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_stadium_teams_team` FOREIGN KEY (`teamId`) REFERENCES `teams` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Beperkingen voor tabel `teams`
--
ALTER TABLE `teams`
  ADD CONSTRAINT `fk_teams_tournament` FOREIGN KEY (`tournamentId`) REFERENCES `tournaments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Beperkingen voor tabel `tournaments`
--
ALTER TABLE `tournaments`
  ADD CONSTRAINT `tournaments_ibfk_2` FOREIGN KEY (`verifiedBy`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Beperkingen voor tabel `tournament_tags`
--
ALTER TABLE `tournament_tags`
  ADD CONSTRAINT `tournament_tags_ibfk_1` FOREIGN KEY (`tournamentId`) REFERENCES `tournaments` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `tournament_tags_ibfk_2` FOREIGN KEY (`tagId`) REFERENCES `tags` (`id`) ON DELETE CASCADE;

--
-- Beperkingen voor tabel `user_roles`
--
ALTER TABLE `user_roles`
  ADD CONSTRAINT `fk_user_roles_role` FOREIGN KEY (`roleId`) REFERENCES `roles` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `fk_user_roles_user` FOREIGN KEY (`userId`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;