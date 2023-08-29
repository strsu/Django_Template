<?php

require_once 'APIClient.php';

session_start();

$success = false;
try {
    $api_client = new APIClient();

    $email = $_POST['email'];
    $password = $_POST['password'];

    $response = $api_client->login($email, $password);

} catch (exception $e) {
    $success = false;
} finally {
    echo (json_encode(array("success" => $success)));
}
?>