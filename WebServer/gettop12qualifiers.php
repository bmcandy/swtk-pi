<?php
// Include database connection
include 'database.php';

// Query to fetch the top 15 qualifiers based on the Best time
$query = "SELECT RawResults.Car,Entries.Driver,Entries.MakeModel,Entries.Class,RawResults.SixtyFour,RawResults.Split,RawResults.Finish,RawResults.Colour FROM RawResults LEFT JOIN Entries ON RawResults.Car=Entries.Car WHERE RawResults.Finish > 0 order by RawResults.Finish Asc limit 15";
$result = mysqli_query($conn, $query);

if (!$result) {
    echo json_encode(["error" => "Database query failed"]);
    exit;
}

$data = [];
while ($row = mysqli_fetch_assoc($result)) {
    $data[] = $row;
}

// Return the data as JSON
header('Content-Type: application/json');
echo json_encode($data);

// Close the database connection
mysqli_close($conn);
?>
