<?php
/* 
* (c) Franky Vanroy 2022
* Script created for Andy Laurence
* Set Limit of shown latest and show ranked
* Connecting to database
*/
// !!!!!!!!Make sure there is a ; after the number !!!!!!
$showlatest = 3; 
$showranked = 10;

$servername = getenv('DB_HOST');
$username = getenv('DB_USER');
$password = getenv('DB_PASSWORD');
$dbname = getenv('DB_NAME');

// Create connection
$conn = mysqli_connect($servername, $username, $password, $dbname) or die("Error " . mysqli_error($conn));
// Check connection
if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

?>
