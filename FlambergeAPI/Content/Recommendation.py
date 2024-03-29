import distance
import pandas as pd
import numpy as np
from Recherche import select_id_film
from connect import clusters_path
df = pd.read_csv(clusters_path, delimiter =",")

df_film_recommende= pd.DataFrame()

id_film="1"

# Fixe l'index sur l'ID du film
df.set_index('idFilm', inplace=True)


# Recherche de film par ID
def chercher_film_par_id(dataframe, film_id):
    try:
        film = dataframe.loc[film_id]
        return film
    except KeyError:
        print(f"Aucun film trouvé avec l'ID {film_id}")
        return None


# Recherche de films par cluster
def chercher_films_par_cluster(dataframe, cluster):
    try:
        films_du_cluster = dataframe[dataframe['cluster'] == int(cluster)]
        if not films_du_cluster.empty:
            return films_du_cluster
        else:
            print(f"Aucun film trouvé dans le cluster {cluster}")
            return None
    except KeyError:
        print(f"Aucun film trouvé dans le cluster {cluster}")
        return None

def meilleur_film(dataframe):
    try:
        # Filtrer les films avec au moins 1000 votes
        films_filtres = dataframe[dataframe['nbVotes'] >= 1000]

        if not films_filtres.empty:
            # Trouver le film le mieux noté parmi ceux filtrés
            film_mieux_note = films_filtres.loc[films_filtres['note'].idxmax()]

            # Retourner le résultat sous forme de DataFrame avec une seule ligne
            return pd.DataFrame([film_mieux_note])
        else:
            print(f"Aucun film avec au moins {1000} votes trouvé.")
            return None
    except ValueError:
        print("Erreur lors de la recherche.")
        return None




def film_aleatoires(dataframe):
    nombre_films = 10

    # Filtrer les films avec une note supérieure à 4.0
    films_filtres = dataframe[dataframe['note'] > 4.0]

    # Vérifier si au moins trois films sont disponibles
    if len(films_filtres) >= nombre_films:
        # Sélectionner trois indices aléatoires
        indices_aleatoires = np.random.choice(films_filtres.index, size=nombre_films, replace=False)

        # Obtenir le sous-DataFrame avec les indices sélectionnés
        films_aleatoires = films_filtres.loc[indices_aleatoires]

        return films_aleatoires
    else:
        print("Il n'y a pas assez de films avec une note supérieure à 4.0.")
        return None


def film_titre_proche(dataframe, film):
    try:
        # Obtenez le titre du film donné
        titre_reference = film['titre'].values[0]

        # Exclure le film avec l'ID donné de la liste des films
        films = dataframe[dataframe.index != film.index[0]].copy()

        # Calculez les distances d'édition avec tous les titres
        films['distance_edit'] = films['titre'].apply(lambda x: distance.levenshtein(titre_reference, str(x)))

        # Trouvez l'index du film avec la distance d'édition la plus basse
        index_plus_proche = films['distance_edit'].idxmin()

        # Récupérez le film correspondant
        films_plus_proche = films.loc[index_plus_proche].copy()

        # Supprimez la colonne temporaire ajoutée pour éviter des problèmes potentiels
        films_plus_proche.drop('distance_edit', inplace=True)

        return pd.DataFrame([films_plus_proche])
    except KeyError:
        print(f"Aucun film trouvé avec l'ID {id_film}")
        return None



# Programme principal
def main():
    while id_film != "-1":
        df_film_recommende= pd.DataFrame()
        # id_film = input("Sur quel film voulez-vous faire la recommandation (id) ? (Entrez -1 pour quitter)\n")
        id_film = select_id_film()

        if id_film != "-1":
            id_film = int(id_film)  # Convertissez l'ID du film en entier

            film_trouve = chercher_film_par_id(df, id_film)

            if film_trouve is not None:
                df_filtre = chercher_films_par_cluster(df, film_trouve["cluster"])

                df_film_recommende = pd.concat([meilleur_film(df_filtre),df_film_recommende])
                df_film_recommende = pd.concat([film_aleatoires(df_filtre),df_film_recommende])
                df_film_recommende = pd.concat([film_titre_proche(df_filtre,id_film),df_film_recommende])
                print("------------- Recommandations ---------------")
                print(df_film_recommende, "\n")


#Fonctions pour API

# df = données chargées au début du programme depuis le csv qui détermine les clusters

def getRecommendation(id_film):
    df_film_recommende= pd.DataFrame()
    id_film = int(id_film)  # Convertissez l'ID du film en entier
    film_trouve = chercher_film_par_id(df, id_film)
    if film_trouve is not None:
        df_filtre = chercher_films_par_cluster(df, film_trouve["cluster"])

        # Exclure le film avec l'ID donné de la liste des films
        film = df_filtre[df_filtre.index == id_film].copy()
        df_filtre = df_filtre[df_filtre.index != id_film].copy()

        df_film_recommende = pd.concat([meilleur_film(df_filtre),df_film_recommende])
        df_film_recommende = pd.concat([film_aleatoires(df_filtre),df_film_recommende])
        df_film_recommende = pd.concat([film_titre_proche(df_filtre,film),df_film_recommende])
        return df_film_recommende
    else :
        return "Aucun film ne possède cet identifiant"
    
def getFilm(id_film):
    try:
        film = df.loc[id_film]
        return film
    except KeyError:
        return "Aucun film ne possède cet identifiant"

def getAllFilm():
    try:
        films = df
        return films
    except KeyError:
        return "Aucun film"

# print(getAllFilm())