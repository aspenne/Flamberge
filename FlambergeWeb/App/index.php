<!DOCTYPE html>
<html lang="fr">

<head>
  <?php require("./film.php") ?>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Accueil</title>
  <link rel="stylesheet" href="style.css">
  <link rel="stylesheet" href="carousel.css">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css"/>
  <link href='https://fonts.googleapis.com/css?family=Biryani' rel='stylesheet'>
  <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/lodash@4.17.21"></script>
  <script src="./sidescroll.js"></script>
  <!-- Swiper JS -->
  <script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
</head>

<body>
  <?php require("./header.php") ?>
  <main>
    <!-- Carroussel amélioré -->
    <section class="laUne">
      <div class="swiper mySwiper">
        <div class="swiper-wrapper">
          <?php
          $numberOfCarouselSlides = 4;

          for ($i = 0; $i < $numberOfCarouselSlides; $i++) {
            $film = getFilmVotes4(); // Sort 4 films avec plus de 300 000 votes pour le carroussel
          ?>
          <div class="swiper-slide">
            <?php $affiche = $film['poster'] ?>
            <div class="img"><a href="details_film.php?idFilm=<?php echo $film["idfilm"]; ?>"><img src="<?php echo $affiche ?>" alt="<?php echo $film['titre']; ?>"></a></div>
            <a href="details_film.php?idFilm=<?php echo $film["idfilm"]; ?>" class="description">
              <h4><?php echo $film['titre']; ?></h4>
              <?php
              if ($film['description'] != '\N') {
                echo "<p>";
                echo $film['description'];
                echo "</p>";
              }
              ?>
              <?php if ($film['note'] != -1) : ?>
                <aside>
                  <?php if ($film['note'] != -1) {
                    echo "<div>", $film['note'], "</div>";
                    echo "<div>★</div>";
                  } ?>
                </aside>
              <?php endif; ?>
            </a>
          </div>
          <?php
          }
          ?>
        </div>
      <div class="swiper-button-next"></div>
      <div class="swiper-button-prev"></div>
      </div>
    </section>

    <section class="film film-section" id="row-1">
      <?php
      // Loop through your existing movies to create placeholders
      for ($i = 0; $i < 20; $i++) { // Adjust the number as needed
        $max = getNumberFilms();
        $film = getFilmById(rand(1, $max['count'])); // Replace with your function to get movie details

        // Limit title length to 20 characters (adjust as needed)
        $limitedTitle = strlen($film['titre']) > 20 ? substr($film['titre'], 0, 20) . '...' : $film['titre'];
      ?>
        <a href="details_film.php?idFilm=<?php echo $film["idfilm"]; ?>">
          <article>
            <!-- Your existing article content -->
            <div class="image-container">
              <?php
              if ($film['isadult'] == 1) {
                $affiche = "./images/poster_moins_18.png";
              } else if ($film['poster'] == '\N') {
                $affiche = "./images/poster_sans_film.png";
              } else {
                $affiche = $film['poster'];
              }
              ?>
              <img src="<?php echo $affiche ?>" alt="<?php echo $limitedTitle; ?>">
            </div>
            <h3><?php echo $limitedTitle; ?></h3>
            <aside>
              <?php if ($film['note'] != -1) {
                echo "<div>", $film['note'], "</div>";
                echo "<div>★</div>";
              } ?>
            </aside>
          </article>
        </a>
      <?php
      }
      ?>
    </section>




    <section class="film film-section" id="row-2">
      <?php
      // Loop through your existing movies to create placeholders
      for ($i = 0; $i < 20; $i++) { // Adjust the number as needed
        $film = getFilmById(rand(1, $max['count'])); // Replace with your function to get movie details
      ?>
        <a href="details_film.php?idFilm=<?php echo $film["idfilm"]; ?>">
          <article>
            <!-- Your existing article content -->
            <?php
              if ($film['isadult'] == 1) {
                $affiche = "./images/poster_moins_18.png";
              } else if ($film['poster'] == '\N') {
                $affiche = "./images/poster_sans_film.png";
              } else {
                $affiche = $film['poster'];
              }
            ?>
            <img src="<?php echo $affiche ?>" alt="<?php echo $film['titre']; ?>">
            <h3><?php echo $film['titre']; ?></h3>
            <aside>
              <?php if ($film['note'] != -1) {
                echo "<div>", $film['note'], "</div>";
                echo "<div>★</div>";
              } ?>
            </aside>
          </article>
        </a>
      <?php
      }
      ?>

    </section>
  </main>

  <button id="retourHaut" onclick="retourEnHaut()"><i class="fa-solid fa-circle-up"></i></button>

  <?php require("./footer.php") ?>
  <script src="./autoSwiper.js"></script>
</body>

</html>