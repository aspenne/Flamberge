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
    dureeminutes VARCHAR(10),
    note FLOAT,
    nbvotes INTEGER
);

DROP TABLE IF EXISTS flamberge_v2._acteur;
create table flamberge_v2._acteur(
	idActeur SERIAL primary key,
	nomartiste Varchar(250)
);

DROP TABLE IF EXISTS flamberge_v2._role;
create table flamberge_v2._role(
	idRole SERIAL primary key,
	nomRole Varchar(250)
);

DROP TABLE IF EXISTS flamberge_v2._genres;
create table flamberge_v2._genres(
	idGenre Serial primary key,
	nomgenre Varchar(250)
);

DROP TABLE IF EXISTS flamberge_v2.temp_csv_data;
CREATE TABLE flamberge_v2.temp_csv_data (
    isadult INTEGER,
    titre VARCHAR(250),
    poster VARCHAR(250),
    description VARCHAR(1000),
    anneesortie INTEGER,
    dureeminutes VARCHAR(10),
    genres VARCHAR(250),
    note FLOAT,
    nbvotes INTEGER,
    role VARCHAR(250),
    nomartiste VARCHAR(250),
    metiers VARCHAR(250)
);

COPY flamberge_v2.temp_csv_data(isadult, titre, poster, description, anneesortie, dureeminutes, genres, note, nbvotes, role, nomartiste, metiers) 
FROM '/data.csv'
WITH (FORMAT CSV, HEADER, DELIMITER ';', NULL '');


INSERT INTO flamberge_v2._film (titre, anneesortie, poster, description, isadult, dureeminutes, note, nbvotes)
  SELECT DISTINCT titre, anneesortie, poster, description, isadult, dureeminutes, note, nbvotes
  FROM flamberge_v2.temp_csv_data;

--import de données dans .flamberge_v2._role--------------------------------

--temp_ma_table(nom de la ou les colonnes du csv)

INSERT INTO flamberge_v2._acteur(nomartiste)
SELECT DISTINCT trim(unnest(string_to_array(nomartiste, ',')))
FROM flamberge_v2.temp_csv_data;

INSERT INTO flamberge_v2._role(nomrole)
SELECT DISTINCT trim(unnest(string_to_array(metiers, ',')))
FROM flamberge_v2.temp_csv_data;




--import de données dans genre--------------------------------------------------------


INSERT INTO flamberge_v2._genres(nomgenre)
SELECT DISTINCT trim(unnest(string_to_array(genres, ',')))
FROM flamberge_v2.temp_csv_data;

DROP TABLE IF EXISTS flamberge_v2._possede_genres;
CREATE TABLE flamberge_v2._possede_genres (
    idfilm INT,
    idgenre INT,
    PRIMARY KEY (idfilm, idgenre),
    CONSTRAINT FK_assos_film FOREIGN KEY (idfilm) REFERENCES flamberge_v2._film(idfilm),
    CONSTRAINT FK_assos_genre FOREIGN KEY (idgenre) REFERENCES flamberge_v2._genres(idgenre)
);



INSERT INTO flamberge_v2._possede_genres (idfilm, idgenre) 
SELECT DISTINCT f.idfilm, g.idgenre
FROM flamberge_v2.temp_csv_data csv
JOIN flamberge_v2._film f ON csv.titre = f.titre
JOIN flamberge_v2._genres g ON g.nomgenre = ANY(string_to_array(csv.genres, ','));


DROP TABLE IF EXISTS flamberge_v2._joue_dans;
create table flamberge_v2._joue_dans(
	idActeur int,
	idFilm int,
	idRole int,
	primary key (idActeur, idFilm, idRole),
    CONSTRAINT FK_assos_film FOREIGN KEY (idfilm) REFERENCES flamberge_v2._film(idfilm),
    CONSTRAINT FK_assos_acteur FOREIGN KEY (idacteur) REFERENCES flamberge_v2._acteur(idacteur),
    CONSTRAINT FK_assos_role FOREIGN KEY (idrole) REFERENCES flamberge_v2._role(idrole)
);

INSERT INTO flamberge_v2._joue_dans(idFilm, idRole, idActeur)
SELECT DISTINCT f.idfilm, r.idrole, a.idacteur
FROM flamberge_v2.temp_csv_data csv
JOIN flamberge_v2._film f ON csv.titre = f.titre
JOIN flamberge_v2._acteur a ON csv.nomartiste = a.nomartiste  
JOIN flamberge_v2._role r ON r.nomrole = ANY(string_to_array(csv.metiers, ','));


DROP TABLE flamberge_v2.temp_csv_data;





