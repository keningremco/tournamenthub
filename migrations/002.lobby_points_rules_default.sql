-- phpMyAdmin SQL Dump
-- version 5.2.2deb1+deb13u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Gegenereerd op: 19 sep 2026 om 20:00
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
-- Tabelstructuur voor tabel `lobby_points_rules_default`
--

CREATE TABLE `lobby_points_rules_default` (
  `perfect_score` int(11) NOT NULL DEFAULT 10,
  `correct_winner` int(11) NOT NULL DEFAULT 5,
  `correct_draw` int(11) NOT NULL DEFAULT 5,
  `exact_team_score` int(11) NOT NULL DEFAULT 2,
  `correct_score_difference` int(11) NOT NULL DEFAULT 3,
  `exact_total_score` int(11) NOT NULL DEFAULT 3
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;

--
-- Gegevens worden geëxporteerd voor tabel `lobby_points_rules_default`
--

INSERT INTO `lobby_points_rules_default` (`perfect_score`, `correct_winner`, `correct_draw`, `exact_team_score`, `correct_score_difference`, `exact_total_score`) VALUES
(10, 5, 5, 2, 3, 3);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
