<?php
try {
    include('./connect.php');
    $dbh = new PDO("$driver:host=$server;port=$port;dbname=$dbname", $user, $pass);
        // $dbh = new PDO("pgsql:host=localhost;port=5601;dbname=flamberge;user=flamberge;password=root"); 
        $dbh -> setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $dbh -> setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
    if (isset($_POST["email"]) && isset($_POST["password"]) && isset($_POST["naissance"])){
        $sth = $dbh->prepare('INSERT INTO flamberge_V2._utilisateur (email, mdp, naissance) VALUES (?, ?, ?)');
        $sth -> execute(array($_POST["email"], $_POST["password"], $_POST["naissance"]));
        unset($_POST);
        header('Location: /connexion.php');        
    } elseif (isset($_POST["email"]) && isset($_POST["mdp"])){
        $sth = $dbh->prepare('SELECT email, naissance FROM flamberge_V2._utilisateur WHERE email = ? AND mdp = crypt(?, mdp)');
        $sth -> execute(array($_POST["email"], $_POST["mdp"]));
        $result = $sth->fetch();
        if ($result){
            $_SESSION["user"]["email"] = $result["email"];
            $_SESSION["user"]["naissance"] = $result["naissance"];
            unset($_POST);
            header('Location: /index.php');
        }
        else {
            header('Location: /connexion.php');
        }
    }

} catch (PDOException $e) {
    
    print "Erreur : " . $e->getMessage() . "<br/>";
    die();
}

?>