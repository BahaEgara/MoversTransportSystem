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
    $password = isset($_POST['password']) ? $_POST['password'] : null;
    $role = isset($_POST['role']) ? $_POST['role'] : null;

    // Check if the required data is available
    if (!$id || !$password || !$role) {
        die("ID, password, and role are required.");
    }

    // Determine which table to query based on the role
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
    $stmt = $conn->prepare("SELECT * FROM $table WHERE ID = ?");
    $stmt->bind_param("i", $id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        if (password_verify($password, $row['password'])) {
            echo "Login successful";
            // Redirect user based on role
            switch ($role) {
                case 'farmer':
                    header("Location: farmerhmpg.html");
                    break;
                case 'retailer':
                    header("Location: retailer.html");
                    break;
                case 'admin':
                    header("Location: adminPanel.html");
                    break;
                case 'driver':
                    header("Location: driver.html");
                    break;
                default:
                    echo "Role not recognized.";
                    break;
            }
        } else {
            echo "Invalid password";
        }
    } else {
        echo "No user found";
    }

    $stmt->close();
}

$conn->close();
?>
