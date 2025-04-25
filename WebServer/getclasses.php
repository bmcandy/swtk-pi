<?php
header('Content-Type: application/json; charset=utf-8');
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: *");

include "database.php";

$sql = "SELECT DISTINCT Class FROM Entries ORDER BY Class ASC";
$result = mysqli_query($conn, $sql) or die("Error fetching classes: " . mysqli_error($conn));

$classes = array();
while ($row = mysqli_fetch_assoc($result)) {
    $classes[] = $row['Class'];
}

echo json_encode($classes);
$conn->close();
?>
