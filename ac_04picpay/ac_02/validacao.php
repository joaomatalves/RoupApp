<?php
if (isset($_POST['enviar'])) {

    if (!empty($_POST['g-recaptcha-response'])){
        $url = "https://www.google.com/recaptcha/api/siteverify";
        $secret = '6LcNt8IlAAAAAFH8Bva0LXtXLAKa7FTt-WO2k-fE';
        $response = $_POST['g-recaptcha-response'];
        $variaveis = "secret=".$secret."&response=".$response;

        $ch = curl_init($url);
        curl_setopt( $ch, CURLOPT_POST, 1);
        curl_setopt( $ch, CURLOPT_POSTFIELDS, $variaveis);
        curl_setopt( $ch, CURLOPT_FOLLOWLOCATION, 1);
        curl_setopt( $ch, CURLOPT_HEADER, 0);
        curl_setopt( $ch, CURLOPT_RETURNTRANSFER, 1);
        $resposta = curl_exec($ch);
        print_r($resposta);
    }
}