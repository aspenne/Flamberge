<?php

use Elasticsearch\ClientBuilder;

try {
    include('./connect.php');
    $dbh = new PDO("$driver:host=$server;port=$port;dbname=$dbname", $user, $pass);
    // $dbh = new PDO("pgsql:host=localhost;port=5601;dbname=flamberge;user=flamberge;password=root"); 
    
    $dbh -> setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $dbh -> setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
} catch (PDOException $e) {
    
    print "Erreur : " . $e->getMessage() . "<br/>";
    die();
}


function getFilmById($id){
    // la fonction qui récupère simplement un film en fonction de son id
    global $dbh;
    $sth = $dbh->prepare('SELECT * from flamberge_V2._film where idFilm = ?');
    $sth -> execute(array($id));
    $films = $sth -> fetchAll();

    return $films[0];
}


function getNumberFilms(){
    // la fonction qui récupère simplement un film en fonction de son id
    global $dbh;
    $sth = $dbh->prepare('SELECT count (idFilm) from flamberge_V2._film');
    $sth -> execute(array());
    $max = $sth -> fetchAll();

    return $max[0];
}

function getFilmVotes4() {
    // renvoie une liste de 4 films avec plus de 300 000 votes
    global $dbh;
    $sth = $dbh->prepare('SELECT * from flamberge_V2._film where nbVotes >= 300000 order by random() limit 4');
    $sth -> execute(array());
    $films = $sth -> fetchAll();
    
    return $films[0];
}

function getBestFilmsByNote(){
    // renvoie une liste de 4 films avec plus de 300 000 votes
    global $dbh;
    $sth = $dbh->prepare('SELECT * from flamberge_V2._film where nbVotes >= 3000 order by note DESC limit 10');
    $sth -> execute(array());
    $films = $sth -> fetchAll();
    
    return $films;
}

function getGenres(){
    // renvoie une liste de 4 films avec plus de 300 000 votes
    global $dbh;
    $sth = $dbh->prepare('SELECT nomGenre, idGenre  from flamberge_V2._genre order by nomGenre ASC');
    $sth -> execute(array());
    $genres = $sth->fetchAll();

    return $genres;
}

function getFilmByGenre($genreId){
    // renvoie une liste de 4 films avec plus de 300 000 votes
    global $dbh;
    $sth = $dbh->prepare('SELECT *
        FROM flamberge_v2._film f
        JOIN flamberge_v2._possede_genre pg ON f.idFilm = pg.idFilm
        JOIN flamberge_v2._genre g ON pg.idGenre = g.idGenre
        WHERE g.idGenre = ? limit 10');
    $sth -> execute(array($genreId));
    $films = $sth -> fetchAll();
    
    return $films;
}

function getBestFilmsByNoteFromElastic() {
    $client = ClientBuilder::create()->build();

    // Définissez votre requête Elasticsearch pour récupérer les films
    $params = [
        'index' => 'votre_index',
        'body' => [
            'query' => [
                'bool' => [
                    'filter' => [
                        'range' => [
                            'nbVotes' => ['gte' => 3000] // "gte" signifie "greater than or equal to"
                        ]
                    ]
                ]
            ],
            'sort' => [
                'note' => ['order' => 'desc'] // Tri par ordre décroissant de la note
            ],
            'size' => 10 // Limite de résultats à 10
        ]
    ];

    // Exécutez la requête Elasticsearch
    $response = $client->search($params);

    // Récupérez les résultats de la recherche
    $films = [];
    foreach ($response['hits']['hits'] as $hit) {
        $films[] = $hit['_source'];
    }

    return $films;
}

?>