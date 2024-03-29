<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>Documentation</title>
    <link rel="stylesheet" type="text/css" href="style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" integrity="sha512-DTOQO9RWCH3ppGqcWaEA1BIZOC6xxalwEsw9c2QQeAIftl+Vegovlnee1c9QX4TctnWMn13TZye+giMm8e2LwA==" crossorigin="anonymous" referrerpolicy="no-referrer" />
</head>

<body>
    <?php require("./header.php") ?>

    <main>
        <h1>Documentation</h1>

        <section class="clickable-section">
    <div class="section-title">
        <h2>Base de données</h2>
        <i class="fas fa-chevron-right arrow-icon"></i>
    </div>
    <div class="content" style="display: none;">
        <p>Nous avons utilisé le CSV de films fourni lors de la première partie, la partie analyse de la SAÉ 5C. 
            Ce fichier ayant assez peu de données, notre base de données est très simpliste.
            Bien que pour cette dernière partie, il nous a fallu la modifier légèrement, car nous avons ajouté les affiches, 
            et les descriptions de films, qui ont été récupérées grâce à du web scraping.
        </p>

        <h4>Tables</h4>
        <p>Les différentes tables sont: </p>
        <ul>
            <li>Film : Cette table possède toutes les données concernant le film lui-même :
                <ul>
                    <li>IdFilm</li>
                    <li>Titre</li>
                    <li>isAdult</li>
                    <li>Poster</li>
                    <li>Description</li>
                    <li>Note</li>
                    <li>NbVotes</li>
                    <li>AnnéeSortie</li>
                </ul>
            </li>

            <li>Artiste : Cette table stocke les informations sur les artistes impliqués dans les films :
                <ul>
                    <li>IdArtiste</li>
                    <li>NomArtiste</li>
                </ul>
            </li>

            <li>Métier : Cette table contient les différentes professions associées aux artistes :
                <ul>
                    <li>IdMetier</li>
                    <li>NomMetier</li>
                </ul>
            </li>

            <li>Exerce_Metier : Cette table représente les associations entre artistes et métiers :
                <ul>
                    <li>IdMetier</li>
                    <li>IdArtiste</li>
                </ul>
            </li>

            <li>Role : Cette table représente les rôles joués par les artistes dans les films :
                <ul>
                    <li>IdFilm</li>
                    <li>IdArtiste</li>
                    <li>NomRole</li>
                </ul>
            </li>

            <li>Genre : Cette table contient les genres associés aux films :
                <ul>
                    <li>IdGenre</li>
                    <li>NomGenre</li>
                </ul>
            </li>

            <li>Possede_Genre : Cette table représente les associations entre films et genres :
                <ul>
                    <li>IdGenre</li>
                    <li>IdFilm</li>
                </ul>
            </li>
        </ul>

        <h4>Relations</h4>
        <p>La base de données contient plusieurs relations entre les tables, notamment :</p>
        <ul>
            <li>La table "Film" est liée à d'autres tables telles que "Genre", "Artiste", "Role", et "Métier" par le biais de clés étrangères.</li>
            <li>La table "Exerce_Metier" établit des relations entre les artistes et les métiers.</li>
            <li>La table "Role" établit des relations entre les films, les artistes, et les rôles joués.</li>
            <li>La table "Possede_Genre" établit des relations entre les films et les genres associés.</li>
        </ul>
    </div>
</section>


<section class="clickable-section">
    <div class="section-title">
        <h2>Système de recommandation</h2>
        <i class="fas fa-chevron-right arrow-icon"></i>
    </div>
    <div class="content" style="display: none;">
        <p>Pour le cœur de notre système de recommandation, nous avons pensé à deux algorithmes possibles :</p>

        <h4>Par similarité item-based</h4>
        <p>
        Le système de recommandation basé sur la similarité item-based repose sur la mesure de la similarité entre les films en se basant sur leurs genres. 
        Pour ce faire, nous avons implémenté plusieurs méthodes comme la distance euclidienne, le cosinus, 
        et le coefficient de Jaccard pour évaluer la similarité entre les vecteurs représentant les genres des films. 
        La méthode présentement utilisée est la distance euclidienne entre 2 vecteurs de genres.
        </p>

        <h4>Grâce à des clusters</h4>
        <p>
            Le système de recommandation basé sur des clusters utilise la méthode K-means pour regrouper les films
            en fonction de leurs vecteurs de genres. Chaque cluster représente un groupe de films similaires.
            <br>
            <br>
            Voici comment nous réalisons le clustering :
            <pre><code class="python">
    <!-- Code de clustering -->
    <span class="python-keyword">import </span><span class="python-library">Donnees</span> <span class="python-keyword">as </span><span class="python-variable">data</span>
    <span class="python-keyword">import </span><span class="python-library">IA_vecteur</span>
    <span class="python-keyword">import </span><span class="python-library">pandas</span> <span class="python-keyword">as</span> <span class="python-variable">pd</span>
    <span class="python-keyword">from </span><span class="python-library">sklearn.cluster</span> <span class="python-keyword">import</span> <span class="python-library">KMeans</span>
    <span class="python-keyword">from </span><span class="python-library">connect</span> <span class="python-keyword">import</span> <span class="python-library">clusters_path</span>
    <span class="python-keyword">from </span><span class="python-library">connect</span> <span class="python-keyword">import</span> <span class="python-library">vecteurs_path</span>
    <span class="python-keyword">import</span> <span class="python-library">json</span>

    <span class="python-comment"># Chargement des données et initialisation</span>
    <span class="python-variable">data</span><span class="python-function">.init()</span>
    
    <span class="python-variable">dfGenres</span> = <span class="python-variable">data.films_genres</span>.<span class="python-function">groupby(<span class="python-string">'idFilm'</span>)[<span class="python-string">'nomGenre'</span>].agg(<span class="python-string">list</span>).reset_index()</span>
    <span class="python-variable">dfGenres[<span class="python-string">'nomGenre'</span>]</span> = <span class="python-variable">dfGenres[<span class="python-string">'nomGenre'</span>]</span><span class="python-function">.apply(<span class="python-keyword">lambda</span> x: <span class="python-built-in">sorted</span>(<span class="python-variable">x</span>))</span>
    <span class="python-variable">dfGenres[<span class="python-string">'nomGenre'</span>]</span> = <span class="python-variable">dfGenres[<span class="python-string">'nomGenre'</span>]</span><span class="python-function">.apply(<span class="python-keyword">lambda</span> x: <span class="python-string">','</span>.join(<span class="python-variable">x</span>))</span>

    <span class="python-variable">dftout</span> = <span class="python-variable">pd</span>.<span class="python-function">merge(<span class="python-variable">data.films</span>, <span class="python-variable">dfGenres</span>, <span class="python-keyword">on</span>=<span class="python-string">'idFilm'</span>)</span>

    <span class="python-keyword">with</span> <span class="python-variable">open</span>(<span class="python-variable">vecteurs_path</span>, <span class="python-string">"r"</span>) <span class="python-keyword">as</span> <span class="python-variable">fp</span>:
        <span class="python-variable">vecteurs</span> = <span class="python-library">json</span>.<span class="python-function">load(<span class="python-variable">fp</span>)</span>
    <span class="python-variable">vecteurs</span> = {<span class="python-function">int</span>(<span class="python-variable">k</span>): <span class="python-variable">v</span> <span class="python-keyword">for</span> <span class="python-variable">k</span>, <span class="python-variable">v</span><span class="python-keyword">in</span> <span class="python-variable">vecteurs.items()</span>}

    <span class="python-comment"># Effectuer le clustering avec K-means</span>
    <span class="python-variable">kmeans</span> = <span class="python-keyword">KMeans</span>(<span class="python-variable">n_clusters</span>=35)
    <span class="python-variable">clusters</span> = <span class="python-variable">kmeans.fit_predict</span>(<span class="python-function">list</span>(<span class="python-variable">vecteurs.values()</span>))

    <span class="python-variable">dftout[<span class="python-string">'cluster'</span>]</span> = <span class="python-variable">clusters</span>

    <span class="python-comment"># Sauvegarder les clusters dans un fichier CSV</span>
    <span class="python-variable">dftout.to_csv</span>(<span class="python-variable">clusters_path</span>, <span class="python-variable">index</span>=<span class="python-keyword">False</span>)
    <!-- Fin du code de clustering -->
</code></pre>
        <p>
            Au final, même si la méthode par clustering est notre algorithme principale, nous avons implémenté les deux dans notre site.
        </p>
    </div>
</section>


        <section class="clickable-section">
            <div class="section-title">
                <h2>API</h2>
                <i class="fas fa-chevron-right arrow-icon"></i>
            </div>
            <div class="content" style="display: none;">
                <p>Voici l'ensemble des routes composant notre API.</p>

                <h4>Routes</h4>
                <p>
                <strong>/</strong> : Vérifie si l'API est opérationnelle.
                <br>
                <br>
                <strong>/update</strong> : Actualise les clusters et les vecteurs.
                <br>
                <br>
                <strong>/recommandations/{id_film}</strong> : Retourne des recommandations de plusieurs films pour un identifiant de film donné en utilisant la méthode par défaut, les clusters. 
                <br>
                <br>
                <strong>/recommandations/similarite/{id_film}</strong> : Retourne des recommandations de plusieurs films pour un identifiant de film donné en utilisant la méthode de similarité.
                <br>
                <br>
                <strong>/films</strong> : Retourne la liste de tous les films.
                <br>
                <br>
                <strong>/films/{id_film}</strong> : Retourne le film associé à l'identifiant donné.
                <br>
                <br>
                <strong>/films/{id_film}/fiche</strong> : Retourne la fiche complète du film associé à l'identifiant donné (informations de base + acteurs + réalisateurs + autres personnes liées).
                <br>
                <br>
                <strong>/films/genre/{nom_genre}</strong> : Retourne tous les films pour un genre donné (insensible à la casse).
                <br>
                <br>
                <strong>/films/acteur/{id_acteur}</strong> : Retourne les films dans lesquels l'acteur donné a joué.
                <br>
                <br>
                <strong>/films/realisateur/{id_realisateur}</strong> : Retourne les films réalisés par le réalisateur donné.
                <br>
                <br>
                <strong>/films/autreArtiste/{id_artiste}</strong> : Retourne les films dans lesquels l'artiste donné, qui n'est ni acteur ni réalisateur, a participé.
                <br>
                <br>
                <strong>/films/recherche/{titre}</strong> : Retourne des films ayant un titre proche du titre donné.
                <br>
                <br>
                <strong>/genres</strong> : Retourne la liste de tous les genres.
                <br>
                <br>
                <strong>/acteurs/{id_film}</strong> : Retourne la liste des acteurs pour un film donné.
                <br>
                <br>
                <strong>/realisateurs/{id_film}</strong> : Retourne la liste des réalisateurs pour un film donné.
                </p>
            </div>
        </section>


        <section class="clickable-section">
            <div class="section-title">
                <h2>Installation</h2>
                <i class="fas fa-chevron-right arrow-icon"></i>
            </div>
            <div class="content" style="display: none;">
                <p>
                    <strong>Prérequis</strong>
                </p>
                <br>
                <ul>
                    <li><strong>Python 3.9.2</strong> ou supérieur</li>
                    <li><strong>PostgreSQL 13.11</strong> ou supérieur</li>
                    <li><strong>pip 20.3.4</strong> ou supérieur</li>
                    <li><strong>PHP 7.0.33</strong> ou supérieur</li>

                </ul>
                <br>
                <br>

                <p>
                    <strong>Installation des dépendances</strong> 
                    <pre><code>
                        pip install -r requirements.txt
                    </code></pre>
                </p>
            

                <p>
                <strong>.gitignore</strong> 
                <br><br>
                <strong>Partie_3/connect.py</strong> 
                <pre> <code>
                    import psycopg2

                    conn = psycopg2.connect(
                        host=host,
                        database=database,
                        user=user,
                        password=password)

                    schema = "flamberge_V2"

                    clusters_path = "/home/etuinfo/userIUT/Documents/SAE_5/git/SAE_5_Flamberge/Partie_3/clusters.csv"
                    vecteurs_path = "/home/etuinfo/userIUT/Documents/SAE_5/git/SAE_5_Flamberge/Partie_3/vecteurs.json"
                </code></pre>
                </p>

                <p>
                <strong>Partie_4/path.py</strong> 
                <pre> <code>
                    from pathlib import Path

                    partie_3_path = Path("/home/etuinfo/userIUT/Documents/SAE_5/git/SAE_5_Flamberge/Partie_3/").expanduser().resolve()
                </code></pre>
                </p>
                
                <p>
                <strong>Partie_5/connect.php</strong> 
                <pre><code>
                    <?php echo htmlspecialchars("<?php
                    $server = 'host';
                    $driver = 'pgsql';
                    $dbname = 'dbname';
                    $user = 'user';
                    $pass = 'password';
                    ?>")
                    ?></code></pre>
                
                <p>
                Le site web peut être lancé manuellement en activant l'API et le serveur PHP, ou en utilisant le script <strong>start_webSite.sh</strong> pour les systèmes Unix/Linux ou <strong>start_webSite.bat</strong> pour les systèmes Windows.
                <br><br>
                <strong>Lancement de l'API</strong> 
                <br><br>
                Depuis le <strong>root</strong> du projet :
                <br><br>
                <pre><code>
                    python3 -m uvicorn Partie_4.API:app --reload
                </pre></code>
                
                <p>
                <strong>Lancement du serveur PHP</strong> 
                Depuis le <strong>root</strong> du projet :
                <br>
                (Il est important d'utiliser le <strong>port 8080</strong> !!)
                <br>
                <pre><code>
                    php -S localhost:8080 -t Partie_5
                </pre></code>
                
                </p>
            </div>
        </section>
    </main>

    <button id="retourHaut" onclick="retourEnHaut()"><i class="fa-solid fa-circle-up"></i></button>

    <?php require("./footer.php") ?>
</body>

</html>