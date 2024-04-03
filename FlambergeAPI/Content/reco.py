from numpy import dot
from numpy.linalg import norm

import connect as conn
import pandas as pd
import math
from connect import vecteurs_path
from connect import clusters_path
import distance

cur = conn.conn.cursor()

def init():
    
    film_i = info_film_select('The Voyager')
    # print(film_i)
    #penser au try catch pour les cas de film genres
    premier_genre = list(film_i['genres'][0])[0]
    # print(film_i['id'], premier_genre)
    # print(list_film_potentielle(film_i['id'], premier_genre))
    tab = list_film_potentielle(film_i['id'], premier_genre)
    # print(len(tab))
    # print(list(tab[1])[0])
    film2 = []
    # for i in range(len(tab)):
    for i in range(100):
       film2.append(info_film_select(list(tab[i])[0]))
    
    # print(list(film2[0]['artiste'][1])[0])
    # print(film2[0])
    
    # print(film2[1]['id'])
    matrice_film_i = compare_attributs(film_i, film_i)
    # print(matrice_film_i[0])
    matrice_correlation = {}
    for i in range(len(film2)):
        matrice_correlation[film2[i]['id']] = compare_attributs(film_i, film2[i])

    # for id_film, matrice in matrice_correlation.items():
    #     print(matrice[0])
    
    
    # similirité entre matrice_film_i et tous les film de la matrice correlation
    tab_similarite = []
    # for i in range(len(matrice_film_i)):
    for id_film, matrice in matrice_correlation.items():
        # tab_similarite.append((id_film, sim_cos(matrice_film_i[0], matrice[0])))
        tab_similarite.append((id_film, sim_jaccard(matrice_film_i[0], matrice[0])))
    

    tableau_similarite_trie = sorted(tab_similarite, key=lambda x: x[1], reverse=True)
    
    tableau_final = []
    print(tableau_similarite_trie)
    # print(sim_cos([3, 1, 2, 1, 12, 2], [0, 0, 2, 1, 0, 2]))
    
    list_id_film = [t[0] for t in tableau_similarite_trie[:20]]
    print(list_id_film)
    
    return list_id_film


schema = "set schema 'flamberge_v2'"
cur.execute(schema)

def info_film_select(nom_film_selectionne) :

    sql_film = "select idfilm, titre, anneesortie, note, isadult from _film  where titre = '"+nom_film_selectionne +"'"
    # print(sql_film)
    cur.execute(sql_film)
    res_film = cur.fetchall()
    # print(res_film[0])
    
    sql_artiste = "select distinct a.nomartiste from _joue_dans as jd left outer join _artiste a on jd.idartiste  = a.idartiste where jd.idfilm = " + str(res_film[0][0])
    cur.execute(sql_artiste)
    res_artiste = cur.fetchall()
    # print(res_artiste[1][0])
    
    sql_genre = "select g.nomgenre from _possede_genre as pg left outer join _genre g on pg.idgenre = g.idgenre where idfilm = " + str(res_film[0][0])
    cur.execute(sql_genre)
    res_genre = cur.fetchall()
    # print(res_genre[0][0])
    
    dico = {
        'id': "",
        'titre': "",
        'anneeSortie': "",
        'note': "",
        'isAdult': "",
        'artiste': {},
        'genres': {},
    }    
    
    dico['id'] = (res_film[0][0])
    dico['titre'] = (res_film[0][1])
    dico['anneeSortie'] = (res_film[0][2])
    dico['note'] = (res_film[0][3])
    dico['isAdult'] = (res_film[0][4])
    for i in range(len(res_artiste)):
        dico['artiste'][i] = {res_artiste[i][0]}
    for i in range(len(res_genre)):    
        dico['genres'][i] = {res_genre[i][0]}
    
    return dico

# print(info_film_select('The Voyager'))


def list_film_potentielle(id_i, genre_i):
    #On filtre sur le genre pour éviter d'avoir trop de resultat. On perd de l'information surement mais on évite trop de ralentissement
    sql = "SELECT f.titre from _film f inner join _possede_genre pg on f.idfilm = pg.idfilm inner join _genre g on pg.idgenre = g.idgenre where pg.idfilm <> " + str(id_i) +" and nomgenre = '"+genre_i +"' and f.note > 2.5 and f.nbvotes > 50"
    # print(sql)
    cur.execute(sql)
    res = cur.fetchall()
    
    return res



def compare_attributs(film_i, film2):
    # Comparaison des attributs titre, année de sortie, note et isAdult
    attributs_similaires = {
        'titre': 3 if film_i['titre'] == film2['titre'] else 0,
        'anneeSortie': 1 if film_i['anneeSortie'] == film2['anneeSortie'] else 0,
        'note': 2*film2['note'] if film_i['note'] <= film2['note'] else 0,
        'isAdult': 1 if (film_i['isAdult'] == 0 and film2['isAdult'] == 0) or (film_i['isAdult'] > 0 and film2['isAdult'] > 0) else 0
    }
    
    # Comparaison des artistes
    artistes_similaires = 0    
    for i in range(len(film2['artiste'])):
        for j in range(len(film_i['artiste'])):    
            artistes_similaires = artistes_similaires + sum(2 for artiste1 in film_i['artiste'][j] for artiste2 in film2['artiste'][i] if artiste1 == artiste2)
    # print(artistes_similaires)
    
    # Comparaison des genres
    genres_similaires = 0
    for i in range(len(film2['genres'])):
        for j in range(len(film_i['genres'])):
            genres_similaires = genres_similaires + sum(2 for genre1 in film_i['genres'][j] for genre2 in film2['genres'][i] if genre1 == genre2)
    # print(genres_similaires)
    
    
    # Création de la matrice de corrélation
    matrice_correlation = [
        # [attributs_similaires['titre'], attributs_similaires['anneeSortie'], attributs_similaires['note'], attributs_similaires['isAdult'], artistes_similaires, genres_similaires],
        [attributs_similaires['titre'], attributs_similaires['anneeSortie'], attributs_similaires['note'], attributs_similaires['isAdult'], artistes_similaires, genres_similaires]
    ]
    
    return matrice_correlation



    


















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

# User based - ici pas utilisé dans le script 
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



init()

cur.close()