<?php
session_start();

require_once("connection.php");

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $farmerid = $_POST['farmer_ID'];
    $driverId = $_POST['doctor_ID'];
    $appointmentDate = $_POST['appointment_date'];
    $appointmentTime = $_POST['appointment_time'];
    $appointmentStatus = 'Scheduled';

    $sql = "INSERT INTO orders (Farmer_ID, Driver_ID, Appointment_Date, Appointment_Time, Appointment_Status)
            VALUES ('$farmerId', '$driverId', '$appointmentDate', '$appointmentTime', '$appointmentStatus')";

    if ($conn->query($sql) === TRUE) {
        header("Location: farmer_view_order.php");
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>Schedule Appointment</title>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Welcome to AgriTrans</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" />

    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/4.6.1/css/bootstrap.min.css" />
    <link rel="stylesheet" href="appointment.css">
</head>
<body>
<header class="header fixed-top">
    <div class="container">
      <div class="row align-items-center justify-content-between">
        <a href="#home" class="logo">Agri<span>Trans</span></a>

        <div class="right">
          <!-- <form id="search">
            <input type="text" placeholder="Search.." name="search">
            <button type="submit"><i class="fa fa-search"></i></button>
          </form> -->
          <!-- <a href="homepage.php" class="btn">Log out</a> -->
          <div class="dropdown">
            <div class="dropdown-icon">
              <div id="user-icon" class="fas fa-user" style="font-size: 1.5em;"></div>
              <div id="username-display" style="font-size: 1.5em;">
                <?php
                if (isset($_SESSION['username'])) {
                  echo $_SESSION['username'];
                } else {
                  echo 'Welcome, Guest';
                }
                ?>
              </div>
              <div id="dropdown-menu" class="fas fa-caret-down"></div>
            </div>
            <div class="dropdown-content">
              <a href="#">View profile</a>
              <a href="homepage.php">Log out</a>
            </div>
          </div>
          <div id="menu-btn" class="fas fa-bars" style="font-size: 2.5em;"></div>
        </div>
        <div id="side-nav" class="side-nav">
          <ul>
            <button id="close-btn" class="close-btn"><i class="fas fa-xmark" style="color: #000000;"></i></button>   
            <li><a id="logo" href="#home" class="logo">Agri<span>Trans</span></a></li>   
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
            <li><a href="#">Services</a></li>
            <li><a href="#">Contact</a></li>    
          </ul>
        </div>
      </div>
    </div>
</header>    
    <div class="app-form mt-5">
        <h1>Schedule Appointment</h1>
        <form method="post" action="">
            <label for="Farmer_ID">Farmer ID</label>
            <input type="text" name="Farmer_ID" required><br>

            <label for="Driver_ID">Driver ID:</label>
            <input type="text" name="Driver_ID" required><br>

            <label for="appointment_date">Appointment Date:</label>
            <input type="date" name="appointment_date" required><br>

            <label for="appointment_time">Appointment Time:</label>
            <input type="time" name="appointment_time" required><br>

            <button type="submit">Schedule</button>
        </form>
    </div>
    <script src="user_homepage.js"></script>
</body>
</html>
