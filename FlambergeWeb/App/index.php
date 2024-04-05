<?php if (!isset($_SESSION["user"])){
  session_start();
}?>
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
  <!-- Swiper JS -->
  <script src="https://unpkg.com/swiper/swiper-bundle.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
  <script src="loadData.js"></script>
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

    <h1 id="filmGenreTitle" style="align-self: start; margin: 0 10%"> Films Action : </h1>
    <?php 
      $genres = getGenres();
    ?>

    <select class="selectGenre" name="genre" onchange="displaySelectedGenre()">
        <?php foreach ($genres as $genre): ?>
            <option value="<?php echo $genre['idgenre']; ?>"><?php echo $genre['nomgenre']; ?></option>
        <?php endforeach; ?>
    </select>

    <section class="film film-section" id="row-1">
      <?php
      // Loop through your existing movies to create placeholders
      $filmsByGenre = getFilmByGenre(26);
      foreach ($filmsByGenre as $filmByGenre) { // Adjust the number as needed
        
      ?>
        <a href="details_film.php?idFilm=<?php echo $filmByGenre["idfilm"]; ?>">
          <article>
            <!-- Your existing article content -->
            <?php
              if ($filmByGenre['isadult'] == 1) {
                $affiche = "./images/poster_moins_18.png";
              } else if (!str_starts_with($filmByGenre['poster'], 'http')) {
                $affiche = "./images/poster_sans_film.png";
              } else {
                $affiche = $filmByGenre['poster'];
              }
            ?>
            <img src="<?php echo $affiche ?>" alt="<?php echo $filmByGenre['titre']; ?>">
            <h3><?php echo $filmByGenre['titre']; ?></h3>
            <aside>
              <?php if ($filmByGenre['note'] != -1) {
                echo "<div>", $filmByGenre['note'], "</div>";
                echo "<div>★</div>";
              } ?>
            </aside>
          </article>
        </a>
      <?php
      }
      ?>

    </section>

    <h1 style="align-self: start; margin: 0 10%"> Film les mieux notés</h1>

    <section class="film film-section" id="row-2">
      <?php
      // Loop through your existing movies to create placeholders
      $filmsByNote = getBestFilmsByNote();
      foreach ($filmsByNote as $filmByNote) { // Adjust the number as needed
        
        //$film = getFilmById(rand(1, $max['count'])); // Replace with your function to get movie details
      ?>
        <a href="details_film.php?idFilm=<?php echo $filmByNote["idfilm"]; ?>">
          <article>
            <!-- Your existing article content -->
            <?php
              if ($filmByNote['isadult'] == 1) {
                $affiche = "./images/poster_moins_18.png";
              } else if (!str_starts_with($filmByNote['poster'], 'http')) {
                $affiche = "./images/poster_sans_film.png";
              } else {
                $affiche = $filmByNote['poster'];
              }
            ?>
            <img src="<?php echo $affiche ?>" alt="<?php echo $filmByNote['titre']; ?>">
            <h3><?php echo $filmByNote['titre']; ?></h3>
            <aside>
              <?php if ($filmByNote['note'] != -1) {
                echo "<div>", $filmByNote['note'], "</div>";
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

<script>

function loadFilmByGenreInPage(selectedGenreId) {
  fetch('http://localhost:8081/films/genre/' + selectedGenreId)
      .then(response => response.json())
      .then(data => {
          const films = data.films;
          const filmSection = document.querySelector('#row-1');

          // Effacer d'abord le contenu actuel de la section des films
          filmSection.innerHTML = '';

          // Boucler à travers les films et les insérer dans la section des films
          films.forEach(film => {
              const filmArticle = document.createElement('article');
              filmArticle.innerHTML = `
                  <a href="details_film.php?idFilm=${film.idFilm}">
                    <article>
                    <img src="${film.poster.startsWith('http') ? film.poster : './images/poster_sans_film.png'}" alt="${film.titre}">
                      <h3>${film.titre}</h3>
                      <aside>
                          <div>${film.note}</div>
                          <div>★</div>
                      </aside>
                    </article>
                  </a>
              `;
              filmSection.appendChild(filmArticle); // Ajouter l'élément filmArticle à la section des films
          });
      })
      .catch(error => console.error('Erreur lors du chargement des films :', error));
}


function displaySelectedGenre() {
    var selectedGenre = document.querySelector('.selectGenre').value;
    var genreName = document.querySelector('option[value="' + selectedGenre + '"]').textContent;

    var filmHeader = document.querySelector('#filmGenreTitle');
    filmHeader.textContent = "Films " + genreName + " : ";

    loadFilmByGenreInPage(genreName);
}
</script>

</html>