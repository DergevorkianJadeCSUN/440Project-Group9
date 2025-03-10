CREATE DATABASE IF NOT EXISTS `project-db`;
USE `project-db`;
CREATE TABLE IF NOT EXISTS `user` (
	`username` varchar(50) NOT NULL,
    `password` varchar(50) NOT NULL,
    `firstName` varchar(50) NOT NULL,
    `lastName` varchar(50),
    `email` varchar(50) NOT NULL UNIQUE,
    `phone` varchar(30) NOT NULL UNIQUE
)