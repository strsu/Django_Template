<?php
class APIClient {
    private $api_url = "http://backend:8000/api/v1";

    public function login($email, $password) {
        $post_data = json_encode(array(
            'email' => $email,
            'password' => $password
        ));
        $response = $this->sendRequest('POST', "user/token/", $post_data);

        if(isset($response['access'])) {
            $_SESSION["access"] = $response["access"];
            $_SESSION["refresh"] = $response["refresh"];
            return true;
        }

        return false;
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
?>