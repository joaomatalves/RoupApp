# Python standard libraries
import json
import os
import sqlite3

from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User

from flask import Flask, redirect, request, url_for


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

# Third party libraries

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return "Você deve estar logado pra acessar esse conteudo.", 403


try:
    init_db_command()
except sqlite3.OperationalError:
    pass


client = WebApplicationClient(GOOGLE_CLIENT_ID)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route('/')
def index():
    if current_user.is_authenticated:
        return (
            "<p>Olá, {}! Você está logado! Email: {}</p>"
            "<div><p>Foto do perfil do Google: </p>"
            '<img src="{}" alt="Google profile pic"></img></div>'
            '<div><p>Gostaria de sair realmente da sua conta?</p>'
            '<a class="button" href="/logout">Sair</a>'.format(
                current_user.name, current_user.email, current_user.profile_pic
            )
        )
    else:
        return '<a class="button" href="/login">Google Login</a>'


@app.route('/login')
def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=['openid', 'email', 'profile']
    )
    return redirect(request_uri)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route('/login/callback')
def callback():
    code = request.args.get('code')

    google_provider_cfg = get_google_provider_cfg()

    token_endpoint = google_provider_cfg['token_endpoint']

    # Prepara a requisição para obter o token de acesso
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )

    # Faz a requisição para obter o token de acesso
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
    )

    # Analisa a resposta da requisição de token e atualiza o estado do cliente
    client.parse_request_body_response(json.dumps(token_response.json()))

    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']

    # Adiciona o token de acesso à requisição para o endpoint de userinfo
    uri, headers, body = client.add_token(userinfo_endpoint)

    # Faz a requisição para o endpoint de userinfo para obter informações do usuário
    userinfo_response = requests.get(uri, headers=headers, data=body)
    print(userinfo_response.json())

    if userinfo_response.json().get('email_verified'):
        unique_id = userinfo_response.json()['sub']
        users_email = userinfo_response.json()['email']
        picture = userinfo_response.json()['picture']
        users_name = userinfo_response.json()['given_name']
    else:
        return "Email não valido ou não verificado pelo google", 400

    user = User(id_=unique_id, name=users_name, email=users_email, profile_pic=picture)

    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    login_user(user)

    return redirect('http://127.0.0.1:5500/ac_02/catalogo.html')


@app.route('/logout')
def logout():
    # Logout do usuário
    logout_user()
    # Redirecionar para outro site externo
    return redirect(url_for('index'))
    


if __name__ == "__main__":
    app.run(debug=True)