<?php session_start(); ?>
<!DOCTYPE html>
<html lang="fr">

<head>
  <?php require("./film.php") ?>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ma Page d'Accueil</title>
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
        <?php
        $film = getFilmById(2);
        print_r($film);
        
        echo "\n",$film['poster'];
        ?>
        <img src="<?php echo $film['poster'] ?>" alt="bite">
    </main>

     <?php require("./footer.php") ?>
</body>
</html>