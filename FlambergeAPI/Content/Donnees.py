import pandas as pd
import psycopg2
import connect
import numpy as np

# Connexion à la base de données
conn = connect.conn
cur = conn.cursor()


def init():
    global films, genres, artistes, films_genres, films_roles
    

    #
    # Charger le jeu de données dans une structure de données Pandas (DataFrame).
    #

    # Films
    cur.execute(f"SELECT * FROM {connect.schema}._film")
    films = pd.DataFrame(cur.fetchall())
    films.columns = ['idFilm', 'titre', 'anneeSortie', 'poster', 'description', 'isAdult', 'dureeMinutes', 'note', 'nbVotes']

    # Genres
    cur.execute(f"SELECT * FROM {connect.schema}._genre")
    genres = pd.DataFrame(cur.fetchall())
    genres.columns = ['idGenre', 'nomGenre']

    # Possede-Genres
    cur.execute(f"SELECT * FROM {connect.schema}._possede_genre")
    possede_genres = pd.DataFrame(cur.fetchall())
    possede_genres.columns = ['idGenre', 'idFilm']

    # Artistes
    cur.execute(f"SELECT * FROM {connect.schema}._artiste")
    artistes = pd.DataFrame(cur.fetchall())
    artistes.columns = ['idArtiste', 'nomArtiste']

    # Roles
    cur.execute(f"SELECT * FROM {connect.schema}._role")
    roles = pd.DataFrame(cur.fetchall())
    roles.columns = ['idRole', 'nomRole']

    # Joue_dans
    cur.execute(f"SELECT * FROM {connect.schema}._joue_dans")
    joue_dans = pd.DataFrame(cur.fetchall())
    joue_dans.columns = ['idArtiste', 'idFilm', 'idRole']

    # Films-Genres
    query = """
    SELECT f.idFilm, f.titre, f.anneeSortie, f.poster, f.description, f.isAdult, f.dureeMinutes, f.note, f.nbVotes, g.idGenre, g.nomGenre
    FROM flamberge_v2._film f
    JOIN flamberge_v2._possede_genre pg ON f.idFilm = pg.idFilm
    JOIN flamberge_v2._genre g ON pg.idGenre = g.idGenre;"""
    cur.execute(query)

    films_genres = pd.DataFrame(cur.fetchall(), columns=['idFilm', 'titre', 'anneeSortie', 'poster', 'description', 'isAdult', 'dureeMinutes', 'note', 'nbVotes', 'idGenre', 'nomGenre'])

    film_with_id_role = pd.merge(joue_dans, films, on='idFilm')
    films_roles = pd.merge(film_with_id_role, roles, on='idRole')


init()
#Fonctions pour API


def getActeurs(id_film):
    if id_film in films_roles['idFilm']:
        # Filter the DataFrame based on the provided id_film and roles containing "actor" or "actress"
        actors_data = films_roles[
            (films_roles['idFilm'] == id_film) & 
            (films_roles['nomRole'].str.contains('actor|actress', case=False))
        ]

        # Merge with the "artistes" DataFrame
        merged_result = pd.merge(actors_data, artistes, on="idArtiste", how="left")

        if merged_result.empty:
            return "Aucun acteur ou actrice n'a été trouvé pour ce film."
        else:
            # Extract relevant fields from the merged DataFrame
            actors_list = merged_result[["idArtiste", "nomArtiste", "nomRole"]].to_dict(orient="records")

            return actors_list
    else:
        return "Aucun film ne possède cet identifiant"


def getRealisateurs(id_film):
    if id_film in films_roles['idFilm']:
        # Filter the DataFrame based on the provided id_film and role "director"
        realisateurs_data = films_roles[
            (films_roles['idFilm'] == id_film) & 
            (films_roles['nomRole'].str.contains('director', case=False))
        ]

        # Merge with the "artistes" DataFrame
        merged_result = pd.merge(realisateurs_data, artistes, on="idArtiste", how="left")

        if merged_result.empty:
            return "Aucun réalisateur n'a été trouvé pour ce film."
        else:
            # Extract relevant fields from the merged DataFrame
            realisateurs_list = merged_result[["idArtiste", "nomArtiste", "nomRole"]].to_dict(orient="records")

            return realisateurs_list
    else:
        return "Aucun film ne possède cet identifiant"

def autresArtistes(id_film):
    if id_film in films_roles['idFilm']:
        artistes_data = films_roles[
            (films_roles['idFilm'] == id_film) & 
            (films_roles['nomRole'].str.contains('actor|actress|director', case=False) == False)
        ]
        
        merged_result = pd.merge(artistes_data, artistes, on="idArtiste", how="left")
        
        if merged_result.empty:
            return "Aucun autre artiste n'a été trouvé pour ce film."
        else:
            artistes_list = merged_result[["idArtiste", "nomArtiste", "nomRole"]].to_dict(orient="records")
            
            return artistes_list
    else:
        return "Aucun film ne possède cet identifiant"

def getFilmById(id_film):
    if id_film in films['idFilm']:
        film = films[films['idFilm'] == id_film]
        return film.to_dict(orient="records")
    else:
        return "Aucun film ne possède cet identifiant"

def getFilmComplet(id_film):
    if id_film in films['idFilm']:
        film = films[films['idFilm'] == id_film]        
        filmComplet = film.to_dict(orient="records")
        filmComplet[0]['genres'] = films_genres[films_genres['idFilm'] == id_film]['nomGenre'].to_list()
        filmComplet[0]['artistes'] = {"Acteurs": getActeurs(id_film), "Réalisateur": getRealisateurs(id_film), "Autres": autresArtistes(id_film)}
        return filmComplet
    else:
        return "Aucun film ne possède cet identifiant"
    

def getFilmsAvecActeur(id_acteur):
    if id_acteur in artistes['idArtiste'].unique():
        if ((films_roles['idArtiste'] == id_acteur) & (films_roles['nomRole'].str.contains('actor|actress', case=False))).any():
            films_data = films_roles[
                (films_roles['idArtiste'] == id_acteur) & 
                (films_roles['nomRole'].str.contains('actor|actress', case=False))
            ]
            
            if films_data.empty:
                return "Aucun film n'a été trouvé pour cet acteur ou actrice."
            else:                return films_data[['idFilm', 'titre', 'isAdult', 'anneeSortie', 'poster', 'description', 'dureeMinutes', 'note', 'nbVotes']].to_dict(orient="records")
        else: 
            return "Aucun acteur ou actrice n'a été trouvé avec cet identifiant."
    else:
        return "Aucun artiste ne possède cet identifiant."
        
# acteur = Tom Hanks
# print(getFilmsAvecActeur(171614))
# print(getFilmsAvecActeur(65977))

def getFilmsAvecRealisateur(id_real):
    if id_real in artistes['idArtiste'].unique():
        if ((films_roles['idArtiste'] == id_real) & (films_roles['nomRole'].str.contains('director', case=False))).any():
            films_data = films_roles[
                (films_roles['idArtiste'] == id_real) & 
                (films_roles['nomRole'].str.contains('director', case=False))
            ]
            
            if films_data.empty:
                return "Aucun film n'a été trouvé pour ce réalisateur."
            else:
                return films_data[['idFilm', 'titre', 'isAdult', 'anneeSortie', 'poster', 'description', 'dureeMinutes', 'note', 'nbVotes']].to_dict(orient="records")
        else: 
            return "Aucun réalisateur n'a été trouvé avec cet identifiant."
        
    else:
        return "Aucun artiste ne possède cet identifiant."
    

    
# real = Christopher Nolan
# print(getFilmsAvecRealisateur(55470))

def getFilmsAvecAutreArtiste(id_autre):
    if id_autre in artistes['idArtiste'].unique():
        if ((films_roles['idArtiste'] == id_autre) & (films_roles['nomRole'].str.contains('actor|actress|director', case=False) == False)).any():
            films_data = films_roles[
                (films_roles['idArtiste'] == id_autre) & 
                (films_roles['nomRole'].str.contains('actor|actress|director', case=False) == False)
            ]
            
            if films_data.empty:
                return "Aucun film n'a été trouvé pour cet artiste."
            else:
                return films_data[['idFilm', 'titre', 'isAdult', 'anneeSortie', 'poster', 'description', 'dureeMinutes', 'note', 'nbVotes']].to_dict(orient="records")
        else: 
            return "Aucun autre artiste n'a été trouvé avec cet identifiant."
        
    else:
        return "Aucun artiste ne possède cet identifiant."

def getFilmsGenre(nom_genre):
    if nom_genre in genres['nomGenre'].to_list():
        films = films_genres[films_genres['nomGenre'] == nom_genre]
        films = films[:10]
        return films.to_dict(orient="records")
    else:
        return "Le genre n'existe pas dans la liste des films"

def getGenres():
    genres_list = genres['nomGenre'].to_list()
    return genres_list