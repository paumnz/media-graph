-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 29-07-2024 a las 10:37:01
-- Versión del servidor: 8.0.35-0ubuntu0.22.04.1
-- Versión de PHP: 8.1.2-1ubuntu2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `medias_journalists`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articles`
--

CREATE TABLE `articles` (
  `id` int NOT NULL,
  `journalist_id` int DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `text` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
  `meta` text,
  `media_id` int DEFAULT NULL,
  `url` text,
  `title` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `journalist`
--

CREATE TABLE `journalist` (
  `id` int NOT NULL,
  `name` varchar(600) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `journalist_media`
--

CREATE TABLE `journalist_media` (
  `id` int NOT NULL,
  `journalist_id` int NOT NULL,
  `media_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `media`
--

CREATE TABLE `media` (
  `id` int NOT NULL,
  `name` varchar(600) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `twitter_username` varchar(600) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `description` text,
  `country` varchar(900) DEFAULT NULL,
  `spain_criticism` tinyint(1) DEFAULT NULL,
  `foreign_intervention` tinyint(1) DEFAULT NULL,
  `pro_russia` tinyint(1) DEFAULT NULL,
  `pro_china` tinyint(1) DEFAULT NULL,
  `anti_imperialism` tinyint(1) DEFAULT NULL,
  `chavism` tinyint(1) DEFAULT NULL,
  `castrism` tinyint(1) DEFAULT NULL,
  `sandinism` tinyint(1) DEFAULT NULL,
  `zapatism` tinyint(1) DEFAULT NULL,
  `indigenism` tinyint(1) DEFAULT NULL,
  `panamericanism` tinyint(1) DEFAULT NULL,
  `disinformation` tinyint(1) DEFAULT NULL,
  `progressism` tinyint(1) DEFAULT NULL,
  `comunism` tinyint(1) DEFAULT NULL,
  `nationalism` tinyint(1) DEFAULT NULL,
  `antiglobalism` tinyint(1) DEFAULT NULL,
  `christianism` tinyint(1) DEFAULT NULL,
  `ecology` int DEFAULT NULL,
  `youth` tinyint(1) DEFAULT NULL,
  `official` tinyint(1) DEFAULT NULL,
  `feminism` tinyint(1) DEFAULT NULL,
  `islamism` tinyint(1) DEFAULT NULL,
  `palestine` tinyint(1) DEFAULT NULL,
  `generalist` tinyint(1) DEFAULT NULL,
  `pacifism` tinyint(1) DEFAULT NULL,
  `migration` tinyint(1) DEFAULT NULL,
  `separatism` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `journalist_id` (`journalist_id`),
  ADD KEY `media_id` (`media_id`);

--
-- Indices de la tabla `journalist`
--
ALTER TABLE `journalist`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `journalist_media`
--
ALTER TABLE `journalist_media`
  ADD PRIMARY KEY (`id`),
  ADD KEY `journalist_id` (`journalist_id`),
  ADD KEY `media_id` (`media_id`);

--
-- Indices de la tabla `media`
--
ALTER TABLE `media`
  ADD PRIMARY KEY (`id`),
  ADD KEY `name` (`name`),
  ADD KEY `twitter_username` (`twitter_username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `journalist`
--
ALTER TABLE `journalist`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `journalist_media`
--
ALTER TABLE `journalist_media`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `media`
--
ALTER TABLE `media`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `articles`
--
ALTER TABLE `articles`
  ADD CONSTRAINT `articles_ibfk_1` FOREIGN KEY (`journalist_id`) REFERENCES `journalist` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `articles_ibfk_2` FOREIGN KEY (`media_id`) REFERENCES `media` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `journalist_media`
--
ALTER TABLE `journalist_media`
  ADD CONSTRAINT `journalist_media_ibfk_1` FOREIGN KEY (`journalist_id`) REFERENCES `journalist` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `journalist_media_ibfk_2` FOREIGN KEY (`media_id`) REFERENCES `media` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
