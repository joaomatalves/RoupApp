import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/enviar-sms', methods=['POST'])
def enviar_sms():
    # Dados do seu cliente na Zenvia
    cliente_id = 'fernando8'
    access_token = 'uSuNpPxccSTMuX4f2ZtnYI3RXzgO67EGjBoC'
    url = 'https://api.zenvia.com/v2/channels/sms/messages'

    # Obtendo os dados da mensagem do corpo da requisição
    dados_mensagem = request.get_json()
    numero_destino = dados_mensagem['numero_destino']
    mensagem = dados_mensagem['mensagem']

    # Montando a mensagem JSON
    data = {
        'to': numero_destino,
        'contents': [
            {
                'type': 'text',
                'text': mensagem
            }
        ]
    }
    json_data = json.dumps(data)

    # Enviando a mensagem
    headers = {
        'Content-Type': 'application/json',
        'X-API-Client': cliente_id,
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.post(url, headers=headers, data=json_data)

    # Verificando se a mensagem foi enviada com sucesso
    if response.status_code == 201:
        return jsonify({'status': 'success', 'message': 'Mensagem enviada com sucesso'})
    else:
        return jsonify({'status': 'error', 'message': 'Erro ao enviar mensagem: ' + response.text})
