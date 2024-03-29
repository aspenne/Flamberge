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
    films.columns = ['idFilm', 'titre', 'isAdult', 'annee', 'poster', 'description', 'dureeMinutes', 'note', 'nbVotes']

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
    roles.columns = ['idFilm', 'idArtiste', 'nomRole']


    #
    # Fusionner les DataFrames
    #

    films_genres = pd.merge(films, possede_genres, on='idFilm')
    films_genres = pd.merge(films_genres, genres, on='idGenre')
    # print(films_genres['nomGenre'].value_counts())
    # print(films_genres[['idFilm','titre', 'nomGenre']])

    films_roles = pd.merge(films, roles, on='idFilm')
    #print(films_roles)

    #
    # Nettoyage des données
    #

    # Supprimer les films avec des genres qui ont moins de 1000 films, car ils ne sont pas assez pertinents
    # films_genres = films_genres[films_genres.groupby('nomGenre').nomGenre.transform(len) > 1000]
    # print(films_genres['nomGenre'].value_counts())

    # Supprimer les films qui n'ont pas de genres ("\N")
    films_genres = films_genres[films_genres['nomGenre'] != '\\N']
    # print(films_genres['nomGenre'].value_counts())

    # Supprimer dans les autres DataFrames les films qui ont été supprimés
    films = films[films['idFilm'].isin(films_genres['idFilm'])]
    films_roles = films_roles[films_roles['idFilm'].isin(films_genres['idFilm'])]
    genres = genres[genres['idGenre'].isin(films_genres['idGenre'])]
    possede_genres = possede_genres[possede_genres['idFilm'].isin(films_genres['idFilm'])]
    roles = roles[roles['idFilm'].isin(films_genres['idFilm'])]
    artistes = artistes[artistes['idArtiste'].isin(films_roles['idArtiste'])]


init()
#Fonctions pour API


def getActeurs(id_film):
    if id_film in films_roles['idFilm'].unique():
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
    if id_film in films_roles['idFilm'].unique():
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
    if id_film in films_roles['idFilm'].unique():
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

def getFilmComplet(id_film):
    if id_film in films['idFilm'].unique():
        film = films[films['idFilm'] == id_film]
                
        genresFilm = films_genres[films_genres['idFilm'] == id_film]['nomGenre'].to_list()
        
        filmComplet = film.to_dict(orient="records")
        filmComplet[0]['genres'] = genresFilm
        # filmComplet[0]['artistes'] = {"Acteurs/actrices": getActeurs(id_film)["idArtiste","nomArtiste"], "Réalisateur": getRealisateurs(id_film)["idArtiste","nomArtiste"], "Autres": autresArtistes(id_film)}
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
            else:
                return films_data[['idFilm', 'titre', 'isAdult', 'annee', 'poster', 'description', 'dureeMinutes', 'note', 'nbVotes']].to_dict(orient="records")
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
                return films_data[['idFilm', 'titre', 'isAdult', 'annee', 'poster', 'description', 'dureeMinutes', 'note', 'nbVotes']].to_dict(orient="records")
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
                return films_data[['idFilm', 'titre', 'isAdult', 'annee', 'poster', 'description', 'dureeMinutes', 'note', 'nbVotes']].to_dict(orient="records")
        else: 
            return "Aucun autre artiste n'a été trouvé avec cet identifiant."
        
    else:
        return "Aucun artiste ne possède cet identifiant."

def getFilmsGenre(nom_genre):
    dfGenres = films_genres.groupby('idFilm')['nomGenre'].agg(list).reset_index()
    data = pd.merge(films, dfGenres, on="idFilm", how="left")
    
    # Trier les genres par ordre alphabétique
    data['nomGenre'] = data['nomGenre'].apply(lambda x: sorted(x) if isinstance(x, list) else [])
    # Convertir la liste de genres en chaîne de caractères
    data['nomGenre'] = data['nomGenre'].apply(lambda x: ','.join(x) if isinstance(x, list) else '')

    if data['nomGenre'].str.lower().eq(nom_genre.lower()).any():        
        films_data = data[data['nomGenre'].str.contains(nom_genre, case=False)]
        
        if films_data.empty:
            return "Aucun film n'a été trouvé pour ce genre."
        else:
            films_data = films_data.rename(columns={'nomGenre': 'Genres'})
            
            # Handle NaN values before converting to dictionary
            films_data = films_data.replace({np.nan: None})
            
            return films_data.to_dict(orient="records")
    else:
        return "Le genre n'existe pas dans la liste des films"


def getGenres():
    genres_list = genres['nomGenre'].to_list()
    return genres_list