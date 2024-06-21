<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "agritrans";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Ensure the form has been submitted and data is available
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Get the input data and check if they exist
    $id = isset($_POST['ID']) ? $_POST['ID'] : null;
    $fname = isset($_POST['Fname']) ? $_POST['Fname'] : null;
    $lname = isset($_POST['Lname']) ? $_POST['Lname'] : null;
    $password = isset($_POST['password']) ? $_POST['password'] : null;
    $contact = isset($_POST['contact']) ? $_POST['contact'] : null;
    $gender = isset($_POST['gender']) ? $_POST['gender'] : null;
    $role = isset($_POST['role']) ? $_POST['role'] : null;

    // Check if the required data is available
    if (!$id || !$fname || !$lname || !$password || !$contact || !$gender || !$role) {
        die("All fields are required.");
    }

    // Hash the password before storing it
    $hashed_password = password_hash($password, PASSWORD_DEFAULT);

    // Determine which table to insert into based on the role
    switch ($role) {
        case 'farmer':
            $table = "farmer";
            break;
        case 'retailer':
            $table = "retailer";
            break;
        case 'admin':
            $table = "admin";
            break;
        case 'driver':
            $table = "driver";
            break;
        default:
            die("Invalid role selected.");
    }

    // Prepare the SQL statement to prevent SQL injection
    $stmt = $conn->prepare("INSERT INTO $table (ID, Fname, Lname, password, contact, gender) VALUES (?, ?, ?, ?, ?, ?)");
    $stmt->bind_param("isssss", $id, $fname, $lname, $hashed_password, $contact, $gender);

    if ($stmt->execute()) {
        echo "Registration successful";
        header("Location: login.php");
    } else {
        echo "Error: " . $stmt->error;
    }

    $stmt->close();
}

$conn->close();
?>
