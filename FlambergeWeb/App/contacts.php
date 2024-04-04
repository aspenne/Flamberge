<?php if (!isset($_SESSION["user"])){
  session_start();
}?>
<!DOCTYPE html>
<html>

<head>
  <meta charset="utf-8">
  <title>Contacts</title>
  <link rel="stylesheet" type="text/css" href="style.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>

<body>
  <?php require("./header.php") ?>

  <main>

    <h1>Contacts</h1>

    <aside class="presentation">
  <p>Nous sommes trois étudiants, originellement <span id="valerian">quatre</span>, actuellement en 3ème année du BUT Informatique à l'IUT de Lannion.</p>
  <br>
  <p>Dans le cadre de notre SAÉ 5C, nous avons entrepris la création d'un système de recommandation de films, intégré de manière transparente à ce site grâce à une API soigneusement mise en place.</p>
  <p>Dans le but de nous distinguer dans le concours, nous mettons en œuvre des algorithmes avancés et des techniques de traitement de données innovantes pour concevoir le meilleur système de recommandation. Notre équipe est animée par la passion de relever ce défi compétitif et de faire une contribution significative au domaine des recommandations de films.</p>
  <hr>
  <p>Pour toute communication, n'hésitez pas à nous contacter par mail ou sur Discord en utilisant les liens suivants :</p>
</aside>

    <article>
      <h2>Erwan FERTRAY</h2>
      <a href="mailto:erwan.fertray@etudiant.univ-rennes1.fr"><i class="fa fa-envelope"></i>erwan.fertray@etudiant.univ-rennes1.fr</a>
      <br>
      <a href="https://discord.com/users/429370662612631552" target="_blank" rel="noopener noreferrer"><i class="fa-brands fa-discord"></i>erou22</a>
      <hr>
    </article>

    <article>
      <h2>Evan CARADEC</h2>
      <a href="mailto:evan.caradec@etudiant.univ-rennes1.fr"><i class="fa fa-envelope"></i>evan.caradec@etudiant.univ-rennes1.fr</a>
      <br>
      <a href="https://discord.com/users/299951419417427978" target="_blank" rel="noopener noreferrer"><i class="fa-brands fa-discord"></i>liebherru</a>
      <hr>
    </article>

    <article>
      <h2>Mathéo ALLAIN</h2>
      <a href="mailto:matheo.allain@etudiant.univ-rennes1.fr"><i class="fa fa-envelope"></i>matheo.allain@etudiant.univ-rennes1.fr</a>
      <br>
      <a href="https://discord.com/users/213310416103800832" target="_blank" rel="noopener noreferrer"><i class="fa-brands fa-discord"></i>teyllss </a>
      <hr id="hr-val" style="display: none;">
    </article>

    <article style="display: none;">
      <h2>Valérian GALLE</h2>
      <p>Il n'est plus là, donc à la place il y a <a href="https://youtu.be/EZEfN5z8Mlg">ça</a>.</p>
    </article>
  </main>

  <button id="retourHaut" onclick="retourEnHaut()"><i class="fa-solid fa-circle-up"></i></button>

  <?php require("./footer.php") ?>
</body>

</html>