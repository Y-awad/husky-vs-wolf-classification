<?php

$servername = "127.0.0.1"; 
$username = "root";
$password = "";
$dbname = "reg";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
        die("connection error...". $conn->connect_error);
}
$sql = "INSERT INTO user (name,email) VALUES('".$_POST["name"]."','".$_POST["email"]."')";
if($conn->query($sql)===true){
    echo "new record created";
}else{ echo"error" . $sql . "<br>" . $conn->error;}
$conn->close();

?>