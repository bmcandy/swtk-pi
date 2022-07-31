<?php
/* 
* Pulling Latest runs from database assuming an empty database, ordering by time set 
*/
header('Content-Type: application/json; charset=utf-8');
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: *");
include "database.php";
//SQL Query
$sql = 'SELECT RawResults.Car,Entries.Driver,RawResults.Finish FROM RawResults LEFT JOIN Entries ON RawResults.Car=Entries.Car order by RawResults.Finish;'

$result = mysqli_query($conn, $sql) or die("Error in Selecting " . mysqli_error($conn));
$query = array();
  while ($row = mysqli_fetch_assoc($result)) {
    $query[] = $row;
}
$js= json_encode($query);
echo ($js);
$conn->close();
?>
