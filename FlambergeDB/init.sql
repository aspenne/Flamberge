CREATE EXTENSION IF NOT EXISTS pgcrypto;
DROP SCHEMA IF EXISTS flamberge_V2 CASCADE;
CREATE SCHEMA flamberge_V2;
SET SCHEMA 'flamberge_V2';

-- Tables

CREATE TABLE flamberge_V2._film (
    idFilm SERIAL PRIMARY KEY,
    titre VARCHAR(250) NOT NULL,
    isAdult INTEGER,
    anneeSortie INTEGER,
    poster VARCHAR(250),
    description VARCHAR(1000),
    dureeMinutes VARCHAR(10),
    note FLOAT,
    nbVotes INTEGER
);

CREATE TABLE flamberge_V2._artiste (
    idArtiste SERIAL PRIMARY KEY,
    nomArtiste VARCHAR(75)
);

CREATE TABLE flamberge_V2._metier (
    idMetier SERIAL PRIMARY KEY,
    nomMetier VARCHAR(255)
);

CREATE TABLE flamberge_V2._utilisateur(
  idUser SERIAL PRIMARY KEY,
  email VARCHAR(300) NOT NULL,
  mdp VARCHAR(300) NOT NULL,
  naissance DATE NOT NULL
);

CREATE TABLE flamberge_V2._exerce_metier (
    idMetier INTEGER,
    idArtiste INTEGER,
    CONSTRAINT metier_fk FOREIGN KEY (idMetier) REFERENCES flamberge_V2._metier(idMetier),
    CONSTRAINT artiste_fk FOREIGN KEY (idArtiste) REFERENCES flamberge_V2._artiste(idArtiste),
    CONSTRAINT exerce_metier_pk PRIMARY KEY (idMetier,idArtiste)
);

CREATE TABLE flamberge_V2._role (
    idFilm INTEGER,
    idArtiste INTEGER,
    nomRole VARCHAR(250),
    CONSTRAINT role_film_fk FOREIGN KEY (idFilm) REFERENCES flamberge_V2._film(idFilm),
    CONSTRAINT role_artiste_fk FOREIGN KEY (idArtiste) REFERENCES flamberge_V2._artiste(idArtiste),
    CONSTRAINT role_pk PRIMARY KEY (idFilm,idArtiste,nomRole)
);

CREATE TABLE flamberge_V2._genre (
    idGenre SERIAL PRIMARY KEY,
    nomGenre VARCHAR(255)
);

CREATE TABLE flamberge_V2._possede_genre (
    idGenre INTEGER,
    idFilm INTEGER,
    CONSTRAINT film_fk FOREIGN KEY (idFilm) REFERENCES flamberge_V2._film(idFilm),
    CONSTRAINT genre_fk FOREIGN KEY (idGenre) REFERENCES flamberge_V2._genre(idGenre),
    CONSTRAINT possede_genre_pk PRIMARY KEY (idGenre,idFilm)
);

-- Fonctions

CREATE OR REPLACE FUNCTION flamberge_V2.encrypt_password() RETURNS TRIGGER AS $$
BEGIN
  NEW.mdp = crypt(NEW.mdp, gen_salt('md5'));
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers
CREATE TRIGGER ins_user 
BEFORE INSERT 
ON flamberge_V2._utilisateur 
FOR EACH ROW 
EXECUTE FUNCTION flamberge_V2.encrypt_password();

-- Peuplement

create table flamberge_V2._temp(
    isAdult INTEGER,
    titre VARCHAR(500),
    poster VARCHAR(250),
    description VARCHAR(1000),
    anneeSortie INTEGER,
    dureeMinutes VARCHAR(10),
    genres VARCHAR(100),
    note FLOAT,
    nbVotes INTEGER,
    role varchar(200),
    nomArtiste VARCHAR(75),
    metiers VARCHAR(100)
);

COPY flamberge_V2._temp(isadult, titre, poster, description, anneesortie, dureeminutes, genres, note, nbvotes, role, nomartiste, metiers) 
FROM '/data.csv' 
WITH (FORMAT CSV, HEADER, DELIMITER ';', NULL '');
  
INSERT INTO flamberge_V2._artiste (nomArtiste)
  SELECT DISTINCT nomArtiste
  FROM flamberge_V2._temp;
  
INSERT INTO flamberge_V2._film (titre, isAdult, anneeSortie, poster, description, dureeMinutes, note, nbVotes)
  SELECT DISTINCT titre, isAdult, anneeSortie, poster, description, dureeMinutes, note, nbVotes
  FROM flamberge_V2._temp;

INSERT INTO flamberge_V2._metier (nomMetier)
  SELECT DISTINCT unnest(string_to_array(metiers, ',')) AS nomMetier
  FROM flamberge_V2._temp;

INSERT INTO flamberge_V2._exerce_metier (idArtiste, idMetier)
  SELECT DISTINCT a.idArtiste, m.idMetier
  FROM flamberge_V2._temp t
  JOIN flamberge_V2._artiste a ON t.nomArtiste = a.nomArtiste
  JOIN flamberge_V2._metier m ON m.nomMetier = ANY(string_to_array(t.metiers, ','));
  
INSERT INTO flamberge_V2._genre (nomGenre)
  SELECT DISTINCT unnest(string_to_array(genres, ',')) AS nomGenre
  FROM flamberge_V2._temp;
  
INSERT INTO flamberge_V2._possede_genre (idGenre, idFilm)
  SELECT DISTINCT g.idGenre, f.idFilm
  FROM flamberge_V2._temp t
  JOIN flamberge_V2._film f ON t.titre = f.titre
  JOIN flamberge_V2._genre g ON g.nomGenre = ANY(string_to_array(t.genres, ','));

INSERT INTO flamberge_V2._role (idFilm, idArtiste, nomRole)
  SELECT DISTINCT f.idFilm, a.idArtiste, t.role
  FROM flamberge_V2._temp t
  JOIN flamberge_V2._film f ON t.titre = f.titre
  JOIN flamberge_V2._artiste a ON t.nomArtiste = a.nomArtiste;
  
--DROP TABLE _temp;

-- Views

CREATE OR REPLACE VIEW flamberge_V2.global AS 
  SELECT * FROM flamberge_V2._film NATURAL JOIN flamberge_V2._possede_genre NATURAL JOIN flamberge_V2._genre NATURAL JOIN flamberge_V2._role NATURAL JOIN flamberge_V2._artiste NATURAL JOIN flamberge_V2._exerce_metier NATURAL JOIN flamberge_V2._metier;

CREATE OR REPLACE VIEW flamberge_V2.fgenres AS
  SELECT * from flamberge_V2._film NATURAL JOIN flamberge_V2._possede_genre NATURAL JOIN flamberge_V2._genre;
  
CREATE OR REPLACE VIEW flamberge_V2.fartiste AS
  SELECT * from flamberge_V2._film NATURAL JOIN flamberge_V2._role NATURAL JOIN flamberge_V2._artiste NATURAL JOIN flamberge_V2._exerce_metier NATURAL JOIN flamberge_V2._metier;
  
