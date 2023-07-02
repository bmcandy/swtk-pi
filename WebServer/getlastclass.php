<?php
header('Content-Type: application/json; charset=utf-8');
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: *");
if (!isset($_GET['class'])) {
    echo("[]");
    exit;}
$class = $_GET['class'];
include "database.php";
//SQL Query
$sql = 'SELECT Entries.Driver, sub.Best, Entries.Class FROM ( SELECT Car,Least(COALESCE(Timed1,Timed2),COALESCE(Timed2,Timed1),COALESCE(Timed3,Timed1),COALESCE(Timed4,Timed1)) AS Best from ClassResults where Class = (select Class from Entries where Car=(SELECT Car FROM RawResults order by TimeOfDay Desc LIMIT 1)) order by Best ) sub LEFT JOIN Entries ON sub.Car=Entries.Car order by CASE WHEN Best IS NULL THEN 1 ELSE 0 END ASC, Best Asc';

$result = mysqli_query($conn, $sql) or die("Error in Selecting " . mysqli_error($conn));
$query = array();
  while ($row = mysqli_fetch_assoc($result)) {
    $query[] = $row;
}
$js= json_encode($query);
echo ($js);
$conn->close();
?>
