import pandas as pd
import distance
from connect import clusters_path

df = pd.read_csv(clusters_path, delimiter =",")
# print(df)

def chercher_film_par_titre(dataframe, titre):
    try:
        dataframe["contains"] = dataframe["titre"].str.contains(titre, case=False)
        films = dataframe[dataframe["contains"] == True].copy()
        films['distance_edit'] = films['titre'].apply(lambda x: distance.levenshtein(titre, str(x)))
        if films.empty:
            return f"Aucun film trouvé avec le titre {titre}"
        else:
            films.drop(columns=['contains'], inplace=True)
            return films.sort_values(by=['distance_edit']).head(10).drop(columns=['distance_edit'])
    except KeyError:
        return f"Aucun film trouvé avec le titre {titre}"

def select_id_film():
    titre,film = "", ""
    while titre != "-1":
        titre = input("Sur quel film voulez-vous faire la recommandation (titre) ? (Entrez -1 pour quitter)\n")

        if titre != "-1":
            films_trouves = chercher_film_par_titre(df, titre)
        
            if films_trouves is not None:
                # Montre les films 
                print("------------- Films ---------------")
                for i in range(len(films_trouves)):
                    print(i, " : ", films_trouves.iloc[i]["titre"], " - ", films_trouves.iloc[i]["nomGenre"], " - ", films_trouves.iloc[i]["annee"])
                
                film = input("\nQuel film voulez-vous ? (Entrez -1 pour quitter)\n")
                while not ((film.isdigit() and int(film) >= 0 and int(film) < len(films_trouves)) or film == "-1"):
                    film = input("Quel film voulez-vous ? (Entrez -1 pour quitter)\n")
                if film != "-1":
                    film = int(film)
                
                    return films_trouves.iloc[film]["idFilm"]
                
            else:
                print("Aucun film trouvé")
        
        else:
            return "-1"
                
# print(titre_to_id())