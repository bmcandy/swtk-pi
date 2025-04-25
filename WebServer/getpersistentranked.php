<?php
/* 
* (c) Franky Vanroy 2022
* Script created for Andy Laurence
* Pulling Ranked runs from database
*/
header('Content-Type: application/json; charset=utf-8');
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: *");

include "database.php";

if (isset($_GET['class']) && !empty($_GET['class'])) {
    $class = $_GET['class'];
    $updateQuery = "INSERT INTO LastClass (id, class) VALUES (1, '$class') ON DUPLICATE KEY UPDATE class='$class'";
    mysqli_query($conn, $updateQuery) or die("Error updating last class: " . mysqli_error($conn));
} else {
    $selectQuery = "SELECT class FROM LastClass WHERE id = 1";
    $result = mysqli_query($conn, $selectQuery) or die("Error fetching last class: " . mysqli_error($conn));
    if ($row = mysqli_fetch_assoc($result)) {
        $class = $row['class'];
    } else {
        echo("[]");
        exit;
    }
}

//SQL Query
$sql = 'SELECT Entries.Driver, sub.Best, Entries.Class FROM ( SELECT Car,Least(COALESCE(Timed1,Timed2),COALESCE(Timed2,Timed1),COALESCE(Timed3,Timed1),COALESCE(Timed4,Timed1)) AS Best from ClassResults where Class = "'.$class.'" order by Best ) sub LEFT JOIN Entries ON sub.Car=Entries.Car order by CASE WHEN Best IS NULL THEN 1 ELSE 0 END ASC, Best Asc Limit '.$showranked;

$result = mysqli_query($conn, $sql) or die("Error in Selecting " . mysqli_error($conn));
$query = array();
  while ($row = mysqli_fetch_assoc($result)) {
    $query[] = $row;
}
$js= json_encode($query);
echo ($js);
$conn->close();
?>
