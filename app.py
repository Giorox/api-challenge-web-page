from flask import Flask, render_template
import requests as re

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET"])
def githubLogin():
    '''
    Start Github OAuth2 flow to authenticate a user
    '''
    firstPhaseURL = "https://github.com/login/oauth/authorize"  # First phase URL for OAuth2 authentication
    headers = {"Accept": "application/json"}
    payload = {
        "client_id": "",
        "redirect_uri": "http://127.0.0.1/callback",
        "scope": "user",
        "state": "testestringmudaressamerda"
    }

    firstPhaseResponse = re.get(firstPhaseURL, headers=headers, params=payload)

    return firstPhaseResponse.content


if __name__ == "__main__":
    app.run(debug=True)
