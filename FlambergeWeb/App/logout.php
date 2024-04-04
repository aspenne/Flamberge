<?php
// Start the session
<?php if (!isset($_SESSION["user"])){
    session_start();
  }?>


// Unset all session variables
$_SESSION = array();

// Destroy the session
session_destroy();

// Redirect back to the previous page
header("Location: index.php");
exit;
?>
