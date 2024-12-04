<?php
$servername = "127.0.0.1"; 
$username = "root"; 
$password = ""; 
$dbname = "registration"; 

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$email=$_POST["email"];
$password=$_POST["password"];

$sql = "SELECT password FROM users WHERE email='$email'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $user= $result->fetch_assoc();

    if($password==$user["password"])
    {
        echo "<script> alert('login successful'); </script>";
        
    }
    else echo "<script> alert('invalid password'); </script>";
}
else echo "<script> alert('no user found with this email'); </script>";

$conn->close()
?>
