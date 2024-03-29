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
    </nav>
    <div class="burger-menu" onclick="toggleMenu()">
        <div class="bar"></div>
        <div class="bar"></div>
        <div class="bar"></div>
    </div>
</header>