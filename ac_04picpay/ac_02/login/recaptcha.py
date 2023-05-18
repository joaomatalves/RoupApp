import requests

def verify_recaptcha(response, remote_ip, secret_key):
    url = 'https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret': secret_key,
        'response': response,
        'remoteip': remote_ip
    }
    response = requests.post(url, data=data)
    return response.json()['success']

