CREATE DATABASE IF NOT EXISTS projectdb;
USE projectdb;
CREATE TABLE IF NOT EXISTS user (
	username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    firstName varchar(255) NOT NULL,
    lastName varchar(255),
    email varchar(255) NOT NULL UNIQUE,
    phone varchar(255) NOT NULL UNIQUE,
    PRIMARY KEY (username)
);
INSERT INTO user VALUES ('dummy','$2b$12$OppYXy/.5p0NuGSIQ9E./ecmlbarsYDakKb2hrF5nRw2KA8uF.XyW','Fake','Name','fakeaddress@domain.tld','1-800-555-5555');