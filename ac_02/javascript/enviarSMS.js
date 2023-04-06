function enviarSMS() {
  var numero_destino = document.getElementById('numero_destino').value;

  const MENSAGEM = "RoupApp: Parabéns! Sua compra foi concluída com sucesso."

  var payload = {
      "from": "fernando8",
      "to": numero_destino,
      "contents": [
          {
              "type": "text",
              "text": MENSAGEM
          }
      ]
  };

  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'https://api.zenvia.com/v2/channels/sms/messages', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.setRequestHeader('X-API-Token', 'uSuNpPxccSTMuX4f2ZtnYI3RXzgO67EGjBoC');
  xhr.onreadystatechange = function() {
      if (xhr.readyState === XMLHttpRequest.DONE) {
          if (xhr.status === 200) {
              alert('Seu pedido foi confirmado com sucesso!');
          } else {
              alert('Erro ao enviar mensagem.');
          }
      }
  };
  xhr.send(JSON.stringify(payload));
}
