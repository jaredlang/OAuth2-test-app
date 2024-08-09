from flask import Flask, request, jsonify

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

if __name__ == '__main__':
    app.run(port=5001, debug=True)
