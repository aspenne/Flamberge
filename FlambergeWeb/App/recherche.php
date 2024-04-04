<?php session_start(); ?>
<!DOCTYPE html>
<html lang="fr">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Recherche</title>
  <link rel="stylesheet" href="style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<script> let resultat= "<?php echo $_GET["search"]?>";</script>
  <script src="./loadData.js"></script>
  <script>loadRecherche();</script>
</head>

<body>
  <?php require("./header.php") ?>
  <main>
    <section class="result" id="result">
        <h3> Résultats de recherche pour "<?php echo $_GET["search"] ?>"  </h3>
    </section>
  </main>

  <button id="retourHaut" onclick="retourEnHaut()"><i class="fa-solid fa-circle-up"></i></button>

  <?php require("./footer.php") ?>
</body>
</html>