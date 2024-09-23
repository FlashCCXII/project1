from flask import Flask
from jwks import jwks
from auth import auth

app = Flask(__name__)

# Register endpoints
app.add_url_rule('/jwks', 'jwks', jwks)
app.add_url_rule('/auth', 'auth', auth, methods=['POST'])

if __name__ == '__main__':
    app.run(port=8080)
