<?php
/* 
* (c) Franky Vanroy 2022
* Script created for Andy Laurence
* Pulling Ranked runs from database
*/
header('Content-Type: application/json; charset=utf-8');
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: *");
if (!isset($_GET['class'])) {
    echo("[]");
    exit;}
$class = $_GET['class'];
include "database.php";
//SQL Query
$sql = 'SELECT Entries.Driver, sub.Best, Entries.Class FROM ( SELECT Car,Least(COALESCE(Timed1,Timed2),COALESCE(Timed2,Timed1),COALESCE(Timed3,Timed1),COALESCE(Timed4,Timed1)) AS Best from ClassResults where Class = "'.$class.'" order by Best ) sub LEFT JOIN Entries ON sub.Car=Entries.Car order by Best limit '.$showranked;

$result = mysqli_query($conn, $sql) or die("Error in Selecting " . mysqli_error($conn));
$query = array();
  while ($row = mysqli_fetch_assoc($result)) {
    $query[] = $row;
}
$js= json_encode($query);
echo ($js);
$conn->close();
?>
