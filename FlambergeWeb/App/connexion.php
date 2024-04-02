<!DOCTYPE html>
<html lang="fr">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Connexion</title>
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
    
    <form action="connexion.php" method="post" id="connexion_form">
      <h1>Connexion</h1>
      <div>
        <label for="email">Email* : </label>
        <input type="email" name="email" id="email" required>
      </div>
      <div>
        <label for="password">Mot de passe* : </label>
        <input type="password" name="password" id="password" required>
      </div>
      
      <p>Pas encore de compte ? <a href="inscription.php">Inscrivez-vous</a></p>
      <button type="submit">Se connecter</button>
    </form>
  <button id="retourHaut" onclick="retourEnHaut()"><i class="fa-solid fa-circle-up"></i></button>
  </main>
  <?php require("./footer.php") ?>
</body>

</html>