<?php
// Chaves de autenticação
$picpayToken = 'XXXXXXXXXXXXXXXXXXXX';
$sellerToken = 'XXXXXXXXXXXXXXXXXXXXX';

// Dados da transação
$referenceId = uniqid(); // ID de referência da transação gerado aleatoriamente
$value = 00.01;
//$value = $_POST['value']; Valor da transação
$callbackUrl = 'https://google.com/picpay_callback.php'; // URL para receber notificações de pagamento

// Dados do comprador
$buyerName = $_POST['buyerName'];
$buyerCpf = '12345678900';
$buyerEmail = 'joao@example.com';
$buyerPhone = '5511999999999';

// Montar array com os dados da transação
$payload = array(
    'referenceId' => $referenceId,
    'value' => $value,
    'callbackUrl' => $callbackUrl,
    'buyer' => array(
        'firstName' => $buyerName,
        'document' => $buyerCpf,
        'email' => $buyerEmail,
        'phone' => $buyerPhone
    )
);

// Converter o payload para JSON
$payloadJson = json_encode($payload);

// Configurar a requisição HTTP para criar a transação
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, 'https://appws.picpay.com/ecommerce/public/payments');
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Content-Type: application/json',
    'x-picpay-token: ' . $picpayToken,
    'x-seller-token: ' . $sellerToken
));
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $payloadJson);

// Enviar a requisição e obter a resposta
$response = curl_exec($ch);
curl_close($ch);

// Verificar se a requisição foi bem-sucedida
if ($response === false) {
    echo 'Erro na requisição: ' . curl_error($ch);
} else {
    $responseData = json_decode($response, true);

    // Verificar se a criação da transação foi bem-sucedida
    if (isset($responseData['paymentUrl'])) {
        $paymentUrl = $responseData['paymentUrl'];
        // Redirecionar o comprador para a página de pagamento do PicPay
        header('Location: ' . $paymentUrl);
        exit;
    } else {
        echo 'Erro ao criar transação: ' . $responseData['message'];
    }
}
?>
