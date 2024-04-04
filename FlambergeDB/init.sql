CREATE EXTENSION IF NOT EXISTS pgcrypto;
DROP SCHEMA IF EXISTS flamberge_v2 CASCADE;
CREATE SCHEMA flamberge_v2;
SET SCHEMA 'flamberge_v2';    

DROP TABLE IF EXISTS flamberge_v2._film;
create table flamberge_v2._film(
	idFilm SERIAL PRIMARY KEY,
    titre VARCHAR(250) NOT NULL,
    anneesortie INTEGER,
    poster VARCHAR(250),
    description VARCHAR(1000),
    isadult INTEGER,
    dureeMinutes VARCHAR(10),
    note FLOAT,
    nbVotes INTEGER
);

DROP TABLE IF EXISTS flamberge_v2._artiste;
create table flamberge_v2._artiste(
	idArtiste SERIAL primary key,
	nomArtiste Varchar(250)
);

DROP TABLE IF EXISTS flamberge_v2._role;
create table flamberge_v2._role(
	idRole SERIAL primary key,
	nomRole Varchar(250)
);

DROP TABLE IF EXISTS flamberge_v2._utilisateur;
CREATE TABLE flamberge_v2._utilisateur(
  idUser SERIAL PRIMARY KEY,
  email VARCHAR(300) NOT NULL,
  mdp VARCHAR(300) NOT NULL,
  naissance DATE NOT NULL
);

DROP TABLE IF EXISTS flamberge_v2._exerce_metier;
CREATE TABLE flamberge_v2._exerce_metier (
    idMetier INTEGER,
    idArtiste INTEGER,
    CONSTRAINT metier_fk FOREIGN KEY (idMetier) REFERENCES flamberge_V2._metier(idMetier),
    CONSTRAINT artiste_fk FOREIGN KEY (idArtiste) REFERENCES flamberge_V2._artiste(idArtiste),
    CONSTRAINT exerce_metier_pk PRIMARY KEY (idMetier,idArtiste)

DROP TABLE IF EXISTS flamberge_v2._genre;
create table flamberge_v2._genre(
	idGenre Serial primary key,
	nomGenre Varchar(250)

DROP TABLE IF EXISTS flamberge_v2.temp_csv_data;
CREATE TABLE flamberge_v2.temp_csv_data (
    isAdult INTEGER,
    titre VARCHAR(250),
    poster VARCHAR(250),
    description VARCHAR(1000),
    anneesortie INTEGER,
    dureeMinutes VARCHAR(10),
    genre VARCHAR(250),
    note FLOAT,
    nbVotes INTEGER,
    role VARCHAR(250),
    nomArtiste VARCHAR(250),
    metiers VARCHAR(250)
);

COPY flamberge_v2.temp_csv_data(isadult, titre, poster, description, anneesortie, dureeMinutes, genre, note, nbVotes, role, nomArtiste, metiers) 
FROM '/data.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ';', NULL '');


INSERT INTO flamberge_v2._film (titre, anneesortie, poster, description, isadult, dureeMinutes, note, nbVotes)
  SELECT DISTINCT titre, anneesortie, poster, description, isadult, dureeMinutes, note, nbVotes
  FROM flamberge_v2.temp_csv_data;

--import de données dans .flamberge_v2._role--------------------------------

--temp_ma_table(nom de la ou les colonnes du csv)

INSERT INTO flamberge_v2._artiste(nomArtiste)
SELECT DISTINCT trim(unnest(string_to_array(nomArtiste, ',')))
FROM flamberge_v2.temp_csv_data;

INSERT INTO flamberge_v2._role(nomrole)
SELECT DISTINCT trim(unnest(string_to_array(metiers, ',')))
FROM flamberge_v2.temp_csv_data;




--import de données dans genre--------------------------------------------------------


INSERT INTO flamberge_v2._genre(nomgenre)
SELECT DISTINCT trim(unnest(string_to_array(genre, ',')))
FROM flamberge_v2.temp_csv_data;

DROP TABLE IF EXISTS flamberge_v2._possede_genre;
CREATE TABLE flamberge_v2._possede_genre (
    idFilm INT,
    idGenre INT,
    PRIMARY KEY (idFilm, idGenre),
    CONSTRAINT FK_assos_film FOREIGN KEY (idFilm) REFERENCES flamberge_v2._film(idFilm),
    CONSTRAINT FK_assos_genre FOREIGN KEY (idGenre) REFERENCES flamberge_v2._genre(idGenre)
);


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

INSERT INTO flamberge_v2._possede_genre (idFilm, idGenre) 
SELECT DISTINCT f.idFilm, g.idGenre
FROM flamberge_v2.temp_csv_data csv
JOIN flamberge_v2._film f ON csv.titre = f.titre
JOIN flamberge_v2._genre g ON g.nomgenre = ANY(string_to_array(csv.genre, ','));


DROP TABLE IF EXISTS flamberge_v2._joue_dans;
create table flamberge_v2._joue_dans(
	idArtiste int,
	idFilm int,
	idRole int,
	primary key (idArtiste, idFilm, idRole),
    CONSTRAINT FK_assos_film FOREIGN KEY (idFilm) REFERENCES flamberge_v2._film(idFilm),
    CONSTRAINT FK_assos_artiste FOREIGN KEY (idArtiste) REFERENCES flamberge_v2._artiste(idArtiste),
    CONSTRAINT FK_assos_role FOREIGN KEY (idRole) REFERENCES flamberge_v2._role(idRole)
);

INSERT INTO flamberge_v2._joue_dans(idFilm, idRole, idArtiste)
SELECT DISTINCT f.idFilm, r.idRole, a.idArtiste
FROM flamberge_v2.temp_csv_data csv
JOIN flamberge_v2._film f ON csv.titre = f.titre
JOIN flamberge_v2._artiste a ON csv.nomArtiste = a.nomArtiste  
JOIN flamberge_v2._role r ON r.nomrole = ANY(string_to_array(csv.metiers, ','));


DROP TABLE flamberge_v2.temp_csv_data;
