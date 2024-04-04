<header>
    <div>
        <a href="index.php"><div id="logo"></div></a>
        <div id="search-bar">
            <!-- Ajoutez ici votre code pour la barre de recherche -->
            
            <form action="./recherche.php" method="get">
                <input type="text" placeholder="Rechercher..." name="search">
                <button type="submit" id="search-button"></button>
            </form>
        </div>
    </div>
    <nav>
        <a href="index.php">
            <div>Accueil</div>
        </a>
        <a href="genres.php">
            <div>Genres</div>
        </a>
        <a href="contacts.php">
            <div>Contacts</div>
        </a>
        <a href="documentation.php">
            <div>Documentation</div>
        </a>
        <?php if (($_SERVER["REQUEST_URI"] != "/profil.php")&&($_SERVER["REQUEST_URI"] != "/connexion.php")&&($_SERVER["REQUEST_URI"] != "/inscription.php")) {
            if (isset($_SESSION["user"]["email"])){ ?> 
            <a href="profil.php">
                <img src="./images/account.png" alt="Profil" style="height: 60%; margin-top: 35%;">
            </a>
            <a href="deconnexion.php">
                <section>Déconnexion</section>
            </a>
        <?php } else { ?>
            <a href="connexion.php">
                <section>Connexion</section>
            </a>
        <?php } }?>
    </nav>
    <div class="burger-menu" onclick="toggleMenu()">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
    </div>
</header>