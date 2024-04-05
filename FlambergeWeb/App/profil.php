<?php if (!isset($_SESSION["user"])){
  session_start();
}?>
<!DOCTYPE html>
<html lang="fr">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Profil</title>
  <link rel="stylesheet" href="style.css">
  <link rel="stylesheet" href="carousel.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/lodash@4.17.21"></script>
  <script src="./sidescroll.js"></script>
</head>

<body>
  <?php require("./header.php") ?>
  <main>
    <h1>Bienvenue <?= substr($_SESSION["user"]["email"], 0, strpos($_SESSION["user"]["email"], "@")) ?></h1>
<?php if(strtoupper(substr($_SESSION["user"]["email"], 0, strpos($_SESSION["user"]["email"], "@"))) == "FLAMBERGE") { ?>
    <img src="./images/IMG_6226.jpg" alt="Photo de ultra beaux gosses" style="width: 100%; height: auto;">
<?php } else {?>
    <p>Votre adresse mail : <?= $_SESSION["user"]["email"] ?></p>
    <p>Né le : <?= date("d-m-Y", strtotime($_SESSION["user"]["naissance"])) ?></p>
    <h2>Vos films notés :</h2>
    <p>Vous n'avez pas noté de film pour le moment.</p>
    <?php } ?>
  </main>
    <?php require("./footer.php") ?>
</body>

</html>