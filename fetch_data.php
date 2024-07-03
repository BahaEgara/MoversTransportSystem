<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "AgriTrans";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Function to fetch table data
function fetchTableData($conn, $table) {
    $sql = "SELECT * FROM $table";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        // Manually capitalize the first letter of the table name
        $tableDisplayName = strtoupper(substr($table, 0, 1)) . substr($table, 1);

        echo "<h2>" . $tableDisplayName . "</h2>";
        echo "<table border='1'>";
        echo "<tr>";

        // Fetching column names
        $fieldInfoArray = $result->fetch_fields();
        foreach ($fieldInfoArray as $fieldInfo) {
            echo "<th>{$fieldInfo->name}</th>";
        }

        echo "</tr>";

        // Fetching rows
        while ($row = $result->fetch_assoc()) {
            echo "<tr>";
            foreach ($row as $value) {
                echo "<td>{$value}</td>";
            }
            echo "</tr>";
        }

        echo "</table>";
    } else {
        // Manually capitalize the first letter of the table name
        $tableDisplayName = strtoupper(substr($table, 0, 1)) . substr($table, 1);
        
        echo "<p>No data found for " . $tableDisplayName . ".</p>";
    }
}

// Fetch data for each table
fetchTableData($conn, 'farmer');
fetchTableData($conn, 'driver');
fetchTableData($conn, 'retailer');
fetchTableData($conn, 'admin');

$conn->close();
?>
