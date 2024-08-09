from flask import Flask, request, jsonify
import requests
import os

AUTH_SERVER_URL = os.environ.get('AUTH_SERVER_URL')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')

app = Flask(__name__)

@app.route('/')
def home(): 
    return "Home Page - OAuth2 Test App", 200

@app.route('/health')
def health(): 
    return "OK", 200

@app.route('/callback')
def callback():
    auth_code = request.args.get('code')
    if auth_code:
        return jsonify({"message": "Authorization code received", "code": auth_code})
    else:
        return jsonify({"error": "No authorization code received"}), 400


def get_new_access_token(refresh_token):
    response = requests.post(f'{AUTH_SERVER_URL}/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        return None

@app.route('/data')
def sensitive_data():
    access_token = request.headers.get('Authorization').split(' ')[1]
    refresh_token = request.headers.get('X-Refresh-Token')

    introspection_response = requests.post(f'{AUTH_SERVER_URL}/introspect', data={
        'token': access_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    })
    introspection_data = introspection_response.json()

    if introspection_data['active']:
        return jsonify({"data": "This is very sensitive information", "username": introspection_data['username']})
    else:
        # Token is invalid or expired, try to refresh it
        new_access_token = get_new_access_token(refresh_token)
        if new_access_token:
            return jsonify({"message": "Token refreshed", "new_access_token": new_access_token})
        else:
            return jsonify({"error": "Invalid or expired token, and refresh failed"}), 401


if __name__ == '__main__':
    app.run(port=5001, debug=True)
