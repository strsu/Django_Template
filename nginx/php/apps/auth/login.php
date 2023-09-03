<?php

require_once '../api/api.php';

session_start();

$success = false;
try {
    $api_client = new APIClient();

    $email = $_POST['email'];
    $password = $_POST['password'];

    $response = $api_client->login($email, $password);

    $success = $response;

} catch (exception $e) {
    $success = false;
} finally {
    echo (json_encode(array("success" => $success)));
}
?>