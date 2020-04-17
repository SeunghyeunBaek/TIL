# http flask

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return("You called the service with https")

cert_dir = 'cert/'

if __name__ == '__main__':
    app.run(ssl_context=(cert_dir+'cert.pem', cert_dir+'private_key.pem'))