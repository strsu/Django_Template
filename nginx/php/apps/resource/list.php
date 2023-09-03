<?php

$api_client = new APIClient();

$response = $api_client->sendGetRequest("modelViewSet/");

print_r($response);

?>