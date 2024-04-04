<!DOCTYPE html>
<html lang="fr">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Inscription</title>
  <style>
    .password-container {
      position: relative;
    }

    #password-requirements {
      position: absolute;
      background-color: #fff;
      border: 1px solid #ccc;
      padding: 5px 10px;
      border-radius: 5px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
      color: black;
      width: 125%;
    }
  </style>
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
    <h1>Inscription</h1>
    <form action="compte.php" method="post" onsubmit="return validateForm()" id="inscription_form">
    <div>
      <label for="email">Email* :</label>
      <input type="email" name="email" id="email" required>
    </div>
    <div>
      <label for="naissance">Date de naissance* :</label>
      <input type="date" name="naissance" id="naissance" required>
    </div>
      <div class="password-container">
        <label for="password">Mot de passe* :</label>
        <input type="password" name="password" id="password" required oninput="displayPasswordRequirements()">
        <span id="password-requirements" style="display: none;"></span>
      </div>
      <div>
      <label for="password2">Confirmer le mot de passe* :</label>
      <input type="password" name="password2" id="password2" required>
      </div>
      <p>Déjà un compte ? <a href="connexion.php">Connectez-vous</a></p>

      <button type="submit">S'inscrire</button>
    </form>
  </main>
    <?php require("./footer.php") ?>
  <script>
    function displayPasswordRequirements() {
      let passwordInput = document.getElementById("password");
      let password = passwordInput.value;
      let passwordWidth = passwordInput.offsetWidth;
      let passwordLeft = passwordInput.offsetLeft;

      let uppercaseRegex = /[A-Z]/;
      let specialCharRegex = /[!@#$%^&*(),.?":{}|<>]/;
      let numberRegex = /[0-9]/;

      let requirementsMessage = "";
      let conditions = [];

      if (!uppercaseRegex.test(password)) {
        conditions.push("une lettre majuscule");
      }
      if (!specialCharRegex.test(password)) {
        conditions.push("un caractère spécial");
      }
      if (!numberRegex.test(password)) {
        conditions.push("un chiffre");
      }

      if (conditions.length > 0) {
        requirementsMessage = "Le mot de passe doit contenir au moins : " + conditions.join(", ") + ".";
      }

      let passwordRequirements = document.getElementById("password-requirements");
      
      if (requirementsMessage !== "") {
        passwordRequirements.innerText = requirementsMessage;
        passwordRequirements.style.display = "block";
        passwordRequirements.style.left = passwordLeft + passwordWidth + 10 + "px"; 
      } else {
        passwordRequirements.style.display = "none";
      }
    }

    function validateForm() {
      let mdp = document.getElementById("password").value;
      let mdp2 = document.getElementById("password2").value;
      const birthdate = document.getElementById("naissance").value;

      if (mdp !== mdp2) {
        alert("Les mots de passe ne correspondent pas");
        return false; 
      }

      let uppercaseRegex = /[A-Z]/;
      let specialCharRegex = /[!@#$%^&*(),.?":{}|<>]/;
      let numberRegex = /[0-9]/;

      let conditions = [];

      if (!uppercaseRegex.test(mdp)) {
        conditions.push("une lettre majuscule");
      }
      if (!specialCharRegex.test(mdp)) {
        conditions.push("un caractère spécial");
      }
      if (!numberRegex.test(mdp)) {
        conditions.push("un chiffre");
      }
      console.log(birthdate);
      let ma_diff = Date.now() - new Date(birthdate).getTime();
      let age_dt = new Date(ma_diff);
      let age = Math.abs(age_dt.getUTCFullYear() - 1970);
      if (age < 15) {
        alert("Vous devez avoir au moins 15 ans pour créer un compte.");
        return false;
      }

      if (conditions.length > 0) {
        alert("Le mot de passe doit contenir au moins " + conditions.join(", ") + ".");
        return false; 
      }

      return true;
    }
  </script>
</body>

</html>
