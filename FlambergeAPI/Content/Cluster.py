import Donnees as data
import pandas as pd
from sklearn.cluster import KMeans
from connect import clusters_path
from connect import vecteurs_path
import json


# Chargement des données
def init():
    data.init()
    
    dfGenres = data.films_genres.groupby('idFilm')['nomGenre'].agg(list).reset_index()

    # Trier les genres par ordre alphabétique
    dfGenres['nomGenre'] = dfGenres['nomGenre'].apply(lambda x: sorted(x))

    # Convertir la liste de genres en chaîne de caractères
    dfGenres['nomGenre'] = dfGenres['nomGenre'].apply(lambda x: ','.join(x))

    dftout = pd.merge(data.films, dfGenres, on='idFilm')

    with open(vecteurs_path, "r") as fp:
        vecteurs = json.load(fp)
    vecteurs = {int(k): v for k, v in vecteurs.items()}

    # Effectuer le clustering avec K-means
    kmeans = KMeans(n_clusters=35)
    clusters = kmeans.fit_predict(list(vecteurs.values()))

    # Ajouter les clusters au DataFrame original
    dftout['cluster'] = clusters

    # Sauvegarder les clusters dans un fichier CSV
    dftout.to_csv(clusters_path, index=False)
    
if __name__ == "__main__":
    init()

    # Inertia
    # cost = []
    # for i in range(1, 10):
    #     kmeans = KMeans(n_clusters=i, random_state=42)
    #     kmeans.fit_predict(list(vecteurs.values()))
    #     cost.append(kmeans.inertia_)

    # Afficher le graphique de la méthode du coude
    # plt.plot(range(1, 10), cost, marker='o')
    # plt.xlabel('Number of clusters (K)')
    # plt.ylabel('Inertia (Cost)')
    # plt.title('Elbow Method for Optimal K')
    # plt.show()