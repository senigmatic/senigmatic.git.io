<HTML><H3>
<?php

$name= $_POST["name"];
$contact =  $_POST["contact"]; 

$servername = "us-cdbr-iron-east-01.cleardb.net";
$username = "b8b4ddb5484850";
$password = "c21c00f4";
$dbname = "heroku_2b5d52ba1cda096";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "INSERT INTO users (username, email)
VALUES ('$name','$contact')";

if ($conn->query($sql) === TRUE) {
    echo "Thank you for your interest in the study. Your data has been recorded successfully. Someone from the research team will get in touch with you.";
} else {
	echo "There was an error in recording your data. Please send an email to f003bxq@dartmouth.edu indicating your interest. We will get in touch with you soon.";
    //echo "Error: " . $sql . "<br>" . $conn->error;
}


$conn->close();
?></H3>
</HTML>
