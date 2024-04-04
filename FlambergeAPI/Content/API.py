# python3 -m uvicorn API:app --reload
import pandas as pd
import sys

import Recommendation
import Donnees
import Cluster
import Recherche
import IA_vecteur
import reco

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI() 

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# "Hub" si retourne alors l'API est accessible
@app.get("/")
def read_root():
    return {"L'API": "Fonctione"}

# Met à jour les données et les clusters
@app.get("/update")
def update():
    IA_vecteur.transformation_vecteur()
    Cluster.init()
    return {"Mise à jour": "Terminée"}


# ============================================================================================
# ===================================== Retourne des films ===================================
# ============================================================================================

# Retourne les recommandations d'un film avec le clustering
@app.get("/recommendations/{id_film}")
def read_recommendation(id_film: int):
    recommendations_data = reco.getRecommendation(id_film)
    
    if isinstance(recommendations_data, str):
        # Si il y a un message d'erreur de getRecommendation()
        return JSONResponse(content={"error": recommendations_data}, media_type="application/json", status_code=404)
    else:
        # print(recommendations_data)
        # Récupère les données et stock les données sous forme de dictionnaire
        recommendations_list = []
        for idfilm in recommendations_data:
            recommendations = Donnees.getFilmById(idfilm)
            print(recommendations[0])
            
            recommendation_dict = {
                "idFilm" : idfilm,
                "titre": recommendations[0]["titre"],
                "isAdult" : recommendations[0]["isAdult"],
                "anneeSortie": recommendations[0]["anneeSortie"],
                'poster': recommendations[0]["poster"],
                'description': recommendations[0]["description"],
                'dureeMinutes': recommendations[0]["dureeMinutes"],
                "note": recommendations[0]["note"],
                "nbVotes": recommendations[0]["nbVotes"],
            }
            print(recommendation_dict)
            recommendations_list.append(recommendation_dict)
        
        # Creation d'un dictionnaire avec les recommendations
        result_dict = {"recommendations": recommendations_list}
        # print(result_dict)
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)

# Retourne les recommendations d'un film avec les vecteurs et la similarité Item-based
@app.get("/recommendations/similarite/{id_film}")
def read_recommendation(id_film: int):
    recommendations_data = IA_vecteur.getRecommendation(id_film)
    
    if isinstance(recommendations_data, str):
        # Si il y a un message d'erreur de getRecommendation()
        return JSONResponse(content={"error": recommendations_data}, media_type="application/json", status_code=404)
    else:
        # print(recommendations_data)
        # Récupère les données et stock les données sous forme de dictionnaire
        recommendations_list = []
        for id, row in recommendations_data.iterrows():
            recommendation_dict = {
                "idFilm" : row["idFilm"],
                "titre": str(row["titre"]),
                "isAdult" : row["isAdult"],
                "anneeSortie": row["anneeSortie"],
                'poster': row["poster"],
                'description': row["description"],
                'dureeMinutes': row["dureeMinutes"],
                "note": row["note"],
                "nbVotes": row["nbVotes"],
                "nomGenre": row["nomGenre"]
            }
            recommendations_list.append(recommendation_dict)
        
        # Creation d'un dictionnaire avec les recommendations
        result_dict = {"recommendations": recommendations_list}
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)
    
# Retourne tous les films
@app.get("/films/")
def read_films():
    films_data = Recommendation.getAllFilm()
    # print(films_data)
    if isinstance(films_data, str):
        # Si il y a un message d'erreur de getAllFilm()
        return JSONResponse(content={"error": films_data}, media_type="application/json", status_code=404)
    else : 
        # Récupère les données et stock les données sous forme de dictionnaire
        all_films_list = []
        for id, row in films_data.iterrows():
            all_films_dict = {
                "idFilm" : id,
                "titre": str(row["titre"]),
                "anneeSortie": row["anneeSortie"],
                "note": row["note"],
                "nbVotes": row["nbVotes"],
                "nomGenre": row["nomGenre"]
            }
            all_films_list.append(all_films_dict)
        
        # Creation d'un dictionnaire avec tous les films
        result_dict = {"Films": all_films_list}
        
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)


# Retourne un film
@app.get("/films/{id_film}")
def read_film(id_film: int):
    films_data = Recommendation.getFilm(id_film)
    
    if isinstance(films_data, str):
        # Si il y a un message d'erreur de getFilm()
        return JSONResponse(content={"error": films_data}, media_type="application/json", status_code=404)
    else:
        # Extraction des champs utiles
        titre = str(films_data.get("titre", None))
        isAdult = films_data.get("isAdult", None).item()
        anneeSortie = films_data.get("anneeSortie", None).item()
        poster = films_data.get("poster", None)
        description = films_data.get("description", None)
        dureeMinutes = films_data.get("dureeMinutes", None)
        note = films_data.get("note", None).item()
        nbVotes = films_data.get("nbVotes", None).item()
        nomGenre = films_data.get("nomGenre", None)
        
        # Création d'un dictionnaire avec ces champs
        result_dict = {
            "id film": id_film,
            "titre": titre,
            "isAdult": isAdult,
            "anneeSortie": anneeSortie,
            "poster": poster,
            "description": description,
            "dureeMinutes": dureeMinutes,
            "note": note,
            "nbVotes": nbVotes,
            "nomGenre": nomGenre
        }
        
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)




# Retourne la fiche complète d'un film
@app.get("/films/{id_film}/fiche")
def read_filmFiche(id_film: int):
    film_data = Donnees.getFilmComplet(id_film)
    
    if isinstance(film_data, str):
        # Si il y a un message d'erreur de getFilmComplet()
        return JSONResponse(content={"error": film_data}, media_type="application/json", status_code=404)
    else:
        # Création d'un dictionnaire avec le résultat
        result_dict = {"film": film_data}
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)


# Retourne tous les films d'un acteur
@app.get("/films/acteur/{id_acteur}")
def read_filmsAvecActeur(id_acteur: int):
    films_data = Donnees.getFilmsAvecActeur(id_acteur)
    
    if isinstance(films_data, str):
        # Si il y a un message d'erreur de getFilmsAvecActeur()
        return JSONResponse(content={"error": films_data}, media_type="application/json", status_code=404)
    else:
        # Création d'un dictionnaire avec le résultat
        result_dict = {"films": films_data}
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)


# Retourne tous les films d'un réalisateur
@app.get("/films/realisateur/{id_realisateur}")
def read_filmsAvecRealisateur(id_realisateur: int):
    films_data = Donnees.getFilmsAvecRealisateur(id_realisateur)
    
    if isinstance(films_data, str):
        # Si il y a un message d'erreur de getFilmsAvecRealisateur()
        return JSONResponse(content={"error": films_data}, media_type="application/json", status_code=404)
    else:
        # Création d'un dictionnaire avec le résultat
        result_dict = {"films": films_data}
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)
    

@app.get("/films/autreArtiste/{idArtiste}")
def read_filmsAvecAutreArtiste(idArtiste: int):
    films_data = Donnees.getFilmsAvecAutreArtiste(idArtiste)
    
    if isinstance(films_data, str):
        # Si il y a un message d'erreur de getFilmsAvecAutreArtiste()
        return JSONResponse(content={"error": films_data}, media_type="application/json", status_code=404)
    else:
        # Création d'un dictionnaire avec le résultat
        result_dict = {"films": films_data}
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)
    

# Retourne tous les films avec le genre demandé
@app.get("/films/genre/{nom_genre}")
def read_genre(nom_genre: str):
    films_data = Donnees.getFilmsGenre(nom_genre)
    
    if isinstance(films_data, str):
        # Si il y a un message d'erreur de getFilmsGenre()
        return JSONResponse(content={"error": films_data}, media_type="application/json", status_code=404)
    else:
        # Création d'un dictionnaire avec le résultat
        result_dict = {"films": films_data}
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)
        
# Retourne les 5 films avec le nom le plus proche
@app.get("/films/recherche/{titre}")
def read_recherche(titre: str):
    # Vérifier si un espace est présent dans le titre
    if " " in titre:
        return JSONResponse(content={"error": "Le titre ne doit pas contenir d'espaces"}, media_type="application/json", status_code=400)
    titre = titre.replace("+", " ")
    films_data = Recherche.chercher_film_par_titre(Donnees.films, titre)
    
    if isinstance(films_data, str):
        # Si il y a un message d'erreur de chercher_film_par_titre()
        return JSONResponse(content={"error": films_data}, media_type="application/json", status_code=404)
    else:
        # Création d'un dictionnaire avec le résultat
        films_data = films_data.to_dict(orient="records")
        result_dict = {"films": films_data}
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)

# ============================================================================================
# ==================================== Retourne des acteurs===================================
# ============================================================================================

# Retourne tous les acteurs d'un film
@app.get("/acteurs/{id_film}")
def read_acteurs(id_film: int):
    actors_data = Donnees.getActeurs(id_film)
    
    if isinstance(actors_data, str):
        # Si il y a un message d'erreur de getActeurs()
        return JSONResponse(content={"error": actors_data}, media_type="application/json", status_code=404)
    else:
        # Création d'un dictionnaire avec le résultat
        result_dict = {"actors": actors_data}
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)

# ============================================================================================
# ================================= Retourne des réalisateurs ================================
# ============================================================================================

# Retourne tous les realisateur d'un film
@app.get("/realisateurs/{id_film}")
def read_realisateur(id_film: int):
    directors_data = Donnees.getRealisateurs(id_film)
    
    if isinstance(directors_data, str):
        # Si il y a un message d'erreur de getRealisateurs
        return JSONResponse(content={"error": directors_data}, media_type="application/json", status_code=404)
    else:
        # Création d'un dictionnaire avec le résultat
        result_dict = {"director": directors_data}
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)
    
    
    
# ============================================================================================
# ===================================== Retourne des genres ==================================
# ============================================================================================

# Retourne tous les genres
@app.get("/genres")
def read_genres():
    genres_data = Donnees.getGenres()
    
    if isinstance(genres_data, str):
        # Si il y a un message d'erreur de getGenres()
        return JSONResponse(content={"error": genres_data}, media_type="application/json", status_code=404)
    else:
        # Création d'un dictionnaire avec le résultat
        result_dict = {"genres": genres_data}
        return JSONResponse(content=result_dict, media_type="application/json", status_code=200)