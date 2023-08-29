<?php
class APIClient {
    private $api_url = "http://backend:8000/api/v1";

    public function login($email, $password) {
        $post_data = json_encode(array(
            'email' => $email,
            'password' => $password
        ));
        $response = $this->sendRequest('POST', "user/token/", $post_data);

        if ($response === false) {
            return false;
        } else {
            $_SESSION["access"] = $response["access"];
            $_SESSION["refresh"] = $response["refresh"];
        }

        return true;
    }

    private function refresh() {
        return $this->sendRequest('POST', $url, $data);
    }

    private function getToken() {
        // 세션에서 토큰 가져오기
        return $_SESSION["access"];
    }

    private function sendRequest($method, $url, $data = null) {
        // 헤더 설정
        $headers = array(
            'Content-Type: application/json',
            'Authorization: Bearer ' . $this->getToken() // 세션에서 가져온 토큰 추가
        );

        // cURL 세션 초기화
        $ch = curl_init("{$this->api_url}/{$url}");

        // cURL 옵션 설정
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true); // 응답 값을 반환 받음
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers); // 헤더 설정

        // POST 요청인 경우 설정
        if ($method === 'POST') {
            curl_setopt($ch, CURLOPT_POST, true); // POST 요청 설정
            curl_setopt($ch, CURLOPT_POSTFIELDS, $data); // POST 데이터 설정
        }

        // cURL 실행 및 응답 받기
        $response = curl_exec($ch);

        // cURL 세션 종료
        curl_close($ch);

        // 응답 처리
        if ($response === false) {
            //return "cURL Error: " . curl_error($ch);
            return false;
        } else {
            // JSON 응답 파싱 등을 수행
            return json_decode($response, true);
        }
    }

    public function sendGetRequest($url) {
        return $this->sendRequest('GET', $url);
    }

    public function sendPostRequest($url, $data) {
        return $this->sendRequest('POST', $url, $data);
    }
}

// 세션 시작
session_start();

// API 클라이언트 객체 생성
$api_client = new APIClient($api_url, $token_key);

// GET 요청 보내기
// $response_get = $api_client->sendGetRequest("");
// print_r($response_get);

// POST 요청 보내기 (POST 데이터 예시)
$post_data = json_encode(array(
    'email' => 'admin',
    'password' => 'admin'
));
$response_post = $api_client->login("admin", "admin");
?>
