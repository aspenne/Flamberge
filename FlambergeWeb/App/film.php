<?php

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
    $sth = $dbh->prepare('SELECT * from flamberge_V2._film where idfilm = ?');
    $sth -> execute(array($id));
    $films = $sth -> fetchAll();

    return $films[0];
}


function getNumberFilms(){
    // la fonction qui récupère simplement un film en fonction de son id
    global $dbh;
    $sth = $dbh->prepare('SELECT count (idfilm) from flamberge_V2._film');
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

?>