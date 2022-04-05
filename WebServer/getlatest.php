<?php
/* 
* (c) Franky Vanroy 2022
* Script created for Andy Laurence
* Pulling Latest runs from database
*/
header('Content-Type: application/json; charset=utf-8');
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: *");
include "database.php";
//SQL Query
$sql = 'SELECT RawResults.Car,Entries.Driver,Entries.MakeModel,Entries.Class,RawResults.SixtyFour,RawResults.Split,RawResults.Finish,RawResults.Colour FROM RawResults LEFT JOIN Entries ON RawResults.Car=Entries.Car order by TimeOfDay Desc limit '.$showlatest;

$result = mysqli_query($conn, $sql) or die("Error in Selecting " . mysqli_error($conn));
$query = array();
  while ($row = mysqli_fetch_assoc($result)) {
    $query[] = $row;
}
$js= json_encode($query);
echo ($js);
$conn->close();
?>
