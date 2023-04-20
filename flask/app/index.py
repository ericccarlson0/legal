import os
from flask import Flask, jsonify, request

SSH_DIR = "/Users/ericcarlson/.ssh"

app = Flask(__name__)

@app.route("/")
def index():
    return "raw text"

if __name__ == "__main__":
    app.run(ssl_context=(os.path.join(SSH_DIR, 'cert.pem'), 
                         os.path.join(SSH_DIR, 'key.pem')))
