from numpy import dot
from numpy.linalg import norm

import random
import pandas as pd
import math
import Donnees as data
import time
import json
from connect import vecteurs_path


def transformation_vecteur():
    vecteur = {}
    df_groupe_genre = data.films_genres.groupby("idFilm")["nomGenre"]  # liste des films avec leurs genres sous forme de liste

    for i , row in df_groupe_genre.iterrows() :     # parcours le dataframe des films liés à leurs genres
        idFilm = row["idFilm"]
        genres = row["nomGenre"]
        vecteur[idFilm] = []
        for j in data.genres["nomGenre"] :          # parcours le dataframe des genres
            if (j in genres) : 
                vecteur[idFilm].append(1)
            else : 
                vecteur[idFilm].append(0)
    
    json_data = json.dumps(vecteur)

    with open(vecteurs_path, 'w') as json_file:
        json_file.write(json_data)

    return 0

def sim_eucli(A,B) :
    """
    Similarité sur la distance Euclidienne 
    """
    somme = 0 
    for i in zip(A,B) : 
        somme += (i[0] - i[1]) * (i[0] - i[1])

    if (somme > 0) : 
        rep = 1/math.sqrt(somme)
    else :
        rep = 2
    return rep


def sim_cos(A,B) : 
    """
    Similarité du cosinus 
    """
    return dot(A, B) / (norm(A) * norm(B))


def sim_jaccard(A,B) : 
    """
    Similarité : Coefficient de Jaccard 
    """
    intersection = sum((a and b) for a, b in zip(A, B))
    union = sum((a or b) for a, b in zip(A, B))

    # Éviter une division par zéro
    if union == 0:
        return 0.0

    return intersection / union


# User based - ici pas utilisé dans le script 
def prediction_user(A,B) : 
    """
    vecteur_users : à remplacer par le vecteur des users
    sim :  à remplacer par la fonction de similraité
    note :  à remplacer par les notes mis par users 
    """
    somme_sur = 0
    somme_sous = 0
    liste_users = list(vecteur_users.keys())
    liste_users.remove(A)
    print(liste_users)
    for i in liste_users :  
        # print(i,"  ",note[i][B])
        simi = sim(vecteur_users[A],vecteur_users[i])
        # print(simi)
        somme_sur += note[i][B] * simi
        somme_sous += simi
    
    return somme_sur/somme_sous


# Item based - ici pas utilisé dans le script 

def prediction_item(A,B) : 
    """
    vecteur_items : à remplacer par le vecteur des items
    sim :  à remplacer par la fonction de similraité
    note :  à remplacer par les notes des items 
    """
    somme_sur = 0
    somme_sous = 0
    liste_items = list(vecteur_items.keys())
    liste_items.remove(B)
    print(liste_items)
    for i in liste_items :  
        # print(i,"  ",note[A][i])
        simi = sim(vecteur_items[B],vecteur_items[i])
        # print(simi)
        somme_sur += note[A][i] * simi
        somme_sous += simi
    
    return somme_sur/somme_sous



def recommandation_affichage(nom_film) :
    start = time.time()     # chrono

    with open(vecteurs_path, "r") as fp:
        vecteurs = json.load(fp)
    vecteurs = {int(k): v for k, v in vecteurs.items()}

    recommandation = {}
    id_vecteur = data.films_genres.loc[data.films_genres['titre'].str.lower() == nom_film.lower(), 'idFilm'].values[0]   # Donne l'ID du film selon son titres
    print(id_vecteur)
    for i in list(vecteurs.keys()) :
        recommandation[i] = sim_eucli(vecteurs[id_vecteur], vecteurs[i])   # Similarité entre les différents vecteurs 

    # pour ne pas recommandé le même film
    del recommandation[id_vecteur]

    recommandation_trie = dict(sorted(recommandation.items(), key=lambda item: item[1], reverse = True))  # Trie pour avoir les plus haut taux de similarité en premier
    recommandation_trie_premiers = dict(list(recommandation_trie.items())[:10])     # Sélectionne les 10 premiers éléments pour faire la recommandation 
    
    max_value = max(recommandation_trie.values())
    max_values = [key for key, value in recommandation_trie.items() if value == max_value]

    if len(max_values) > 10 : 
        # Ici on prends les films qui ont la note maximal sur la similarité
        # donc sont égaux, pour ne pas faire resortir les mêmes films en boucle 
        reco_random_top = random.sample(max_values, 10)

        # Montre les films 
        print("------------- Résultats ---------------")
        for i in reco_random_top : 
            print(data.films_genres.loc[data.films_genres['idFilm'] == i, 'titre'].values[0],
            "\n ID film : ", i,
            "\n Genre : ", data.films_genres.loc[data.films_genres['idFilm'] == i, 'nomGenre'].values,
            "\n Taux similarité : ", float(recommandation[i]*100)," %\n")


    else : 
        # Montre les films 
        print("------------- Résultats ---------------")
        for i in recommandation_trie_premiers.items() : 
            print(data.films_genres.loc[data.films_genres['idFilm'] == i[0], 'titre'].values[0],
            "\n ID film : ", i[0],
            "\n Genre : ", data.films_genres.loc[data.films_genres['idFilm'] == i[0], 'nomGenre'].values,
            "\n Taux similarité : ", float(i[1]*100)," %\n")


    # Enlever pour avoir les premiers résultat
    # print("------------- Résultats ---------------")
    # for i in recommandation_trie_premiers.items() : 
    #     print(data.films_genres.loc[data.films_genres['idFilm'] == i[0], 'titre'].values[0],
    #     "\n ID film : ", i[0],
    #     "\n Genre : ", data.films_genres.loc[data.films_genres['idFilm'] == i[0], 'nomGenre'].values,
    #     "\n Taux similarité : ", float(i[1]*100)," %\n")

    stop = time.time() - start

    print("------------- Stats ---------------\nTemps d'execution : ",stop,"\n")

def getRecommendation(id_film) :

    with open(vecteurs_path, "r") as fp:
        vecteurs = json.load(fp)

    vecteurs = {int(k): v for k, v in vecteurs.items()}
    
    recommandation = {}
    for i in list(vecteurs.keys()) :
        recommandation[i] = sim_eucli(vecteurs[id_film], vecteurs[i])   # Similarité entre les différents vecteurs 

    # pour ne pas recommandé le même film
    del recommandation[id_film]

    recommandation_trie = dict(sorted(recommandation.items(), key=lambda item: item[1], reverse = True))  # Trie pour avoir les plus haut taux de similarité en premier
    recommandation_trie_premiers = dict(list(recommandation_trie.items())[:10])     # Sélectionne les 10 premiers éléments pour faire la recommandation 
    
    max_value = max(recommandation_trie.values())
    max_values = [key for key, value in recommandation_trie.items() if value == max_value]

    df_reco = pd.DataFrame()

    if len(max_values) > 10 : 
        # Ici on prends les films qui ont la note maximal sur la similarité
        # donc sont égaux, pour ne pas faire resortir les mêmes films en boucle 
        reco_random_top = random.sample(max_values, 10)

        # res dans dataFrame
        for i in reco_random_top : 

            df = data.films_genres.loc[data.films_genres['idFilm'] == i]
            grouped_df = df.groupby(['idFilm', 'titre']).agg({'idFilm' : 'first', 
                                                              'titre' : 'first', 
                                                              'isAdult': 'first',
                                                              'anneeSortie': 'first', 
                                                              'poster': 'first',
                                                              'description': 'first',
                                                              'dureeMinutes': 'first',
                                                              'note': 'first', 
                                                              'nbVotes': 'first', 
                                                              'idGenre': 'first', 
                                                              'nomGenre': lambda x: ', '.join(x)})
            df_reco = pd.concat([grouped_df,df_reco])    

    else : 
        # res dans dataFrame
         for i in recommandation_trie_premiers.keys() : 
            
            df = data.films_genres.loc[data.films_genres['idFilm'] == i]
            grouped_df = df.groupby(['idFilm', 'titre']).agg({'idFilm' : 'first', 
                                                              'titre' : 'first', 
                                                              'isAdult': 'first',
                                                              'anneeSortie': 'first', 
                                                              'poster': 'first',
                                                              'description': 'first',
                                                              'dureeMinutes': 'first',
                                                              'note': 'first', 
                                                              'nbVotes': 'first', 
                                                              'idGenre': 'first', 
                                                              'nomGenre': lambda x: ', '.join(x)})
            df_reco = pd.concat([grouped_df,df_reco])

    return df_reco

# transformation_vecteur()
# print(getRecommendation(15911))

# Main programme
if __name__ == '__main__' : 
    nom_film = "1"

    while nom_film != "-1" : 
        nom_film = input("Sur quel film voulez vous faire la recommandation (nom du film sans faute ni d'espace après) ? (Entrez -1 pour quitter)\n")

        if nom_film != "-1" :
            getRecommendation(int(nom_film))
        
        else : 
            rep = input("C'est un film ? (y/n) ?\n")
            if (rep == "y") : 
                print("Ce n'est pas bien de mentir, il n'y a pas de films \"-1\" dans cette BDD, il y aura donc une erreur...")
                getRecommendation(nom_film)        # retire si on ne veut pas d'erreur
            else :
                print("Au revoir :(")
