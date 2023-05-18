<?php
// Ler o conteúdo da notificação
$notification = file_get_contents('php://input');

// Decodificar a notificação JSON
$notificationData = json_decode($notification, true);

// Verificar se a notificação é válida
if (isset($notificationData['authorizationId'])) {
    // A notificação é válida, você pode processar as informações do pagamento aqui
    
    // Exemplo: obter o ID da autorização
    $authorizationId = $notificationData['authorizationId'];
    
    // Exemplo: registrar o ID da autorização em um log ou banco de dados
    // ...
    
    // Enviar uma resposta de sucesso ao PicPay
    http_response_code(200);
    echo 'Notificação recebida com sucesso.';
} else {
    // A notificação é inválida ou faltam informações obrigatórias
    // Você pode tratar o erro ou registrar o problema para análise
    
    // Exemplo: registrar o erro em um log ou banco de dados
    // ...
    
    // Enviar uma resposta de erro ao PicPay
    http_response_code(400);
    echo 'Notificação inválida.';
}
?>
