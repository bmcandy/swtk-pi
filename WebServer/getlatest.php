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
$sql = 'SELECT RawResults.car,entries.Driver,entries.MakeModel,entries.Class,RawResults.SixtyFour,rawresults.Split,rawresults.Finish,rawresults.Colour FROM RawResults LEFT JOIN entries ON RawResults.car=entries.car order by TimeOfDay Desc limit '.$showlatest;

$result = mysqli_query($conn, $sql) or die("Error in Selecting " . mysqli_error($conn));
$query = array();
  while ($row = mysqli_fetch_assoc($result)) {
    $query[] = $row;
}
$js= json_encode($query);
echo ($js);
$conn->close();
?>