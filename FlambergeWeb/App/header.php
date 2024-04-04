<header>
    <div>
        <a href="index.php">
            <div id="logo"></div>
        </a>
        <div id="search-bar">
            <form action="./recherche.php" method="get" id="search-form">
                <div id="search-bar-input">
                    <input type="text" id="search-input" placeholder="Rechercher..." name="search">
                    <div id="suggestions-container" class="suggestionsContainer"></div>
                </div>
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
            <a href="logout.php">
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

<script>
    const searchInput = document.getElementById('search-input');
    const suggestionsContainer = document.getElementById('suggestions-container');
    const searchBarInput = document.getElementById('search-bar-input');

    searchInput.addEventListener('input', async () => {
        const inputValue = searchInput.value.trim();
        if (inputValue.length > 0) {
            const suggestions = await searchAutocomplete(inputValue);
            renderSuggestions(suggestions);
        } else {
            clearSuggestions();
        }
    });

    async function fetchSuggestions(query) {
        const response = await fetch(`./recherche.php?search=${query}`);
        return await response.json();
    }

    function renderSuggestions(suggestions) {
        suggestionsContainer.innerHTML = '';
        console.log(suggestions);
        if (Array.isArray(suggestions) && suggestions.length > 0) {
            suggestions.forEach(suggestion => {
                const suggestionElement = document.createElement('div');
                suggestionElement.classList.add('suggestion');
                suggestionElement.addEventListener('click', () => {
                    window.location.href = `details_film.php?idFilm=${suggestion._source.idfilm}`;
                });

                const imageElement = document.createElement('img');
                imageElement.classList.add('suggestionImage');
                if (!suggestion._source.poster.startsWith('http')){
                    imageElement.src = '../images/no_image_available.jpeg';
                } else {
                    imageElement.src = suggestion._source.poster;
                }
                imageElement.alt = 'autocomplete image';

                const textElement = document.createElement('div');
                textElement.classList.add('suggestionText');
                textElement.textContent = suggestion._source.titre;
                
                const noteElement = document.createElement('div');
                if (suggestion._source.note === -1){
                    noteElement.textContent = 'N/A';
                } else {
                    noteElement.classList.add('suggestionNote');
                    noteElement.textContent = suggestion._source.note + '/ 10';
                }

                const suggestionContent = document.createElement('div');
                const suggestionImage = document.createElement('div');
                suggestionImage.appendChild(imageElement);
                suggestionContent.appendChild(textElement);
                suggestionContent.appendChild(noteElement);

                suggestionElement.appendChild(suggestionImage);
                suggestionElement.appendChild(suggestionContent);
                suggestionsContainer.style.display = 'flex';
                suggestionsContainer.appendChild(suggestionElement);

            });
        } else {
            suggestionsContainer.style.display = 'none';
        }
    }

    function clearSuggestions() {
        suggestionsContainer.innerHTML = '';
        suggestionsContainer.style.display = 'none';
    }
</script>
