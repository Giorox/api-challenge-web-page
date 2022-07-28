from flask import Flask, redirect, render_template, request, session
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
    payload = {
        "client_id": "",
        "redirect_uri": "http://127.0.0.1:5000/callback",
        "scope": "user",
        "state": "testestringmudaressamerda"
    }

    # Hand build the request URL for the initial authentication procedure
    url = firstPhaseURL + "?" + '&'.join([f"{param}={value}" for param, value in payload.items()])

    return redirect(url)


@app.route("/callback", methods=["GET"])
def getAuthCallback():
    '''
    Receive Github OAuth2 session information (phase 2) after successful user login
    '''
    state = request.args.get('state')
    code = request.args.get('code')
    print(state, code)
    return state, code


if __name__ == "__main__":
    app.run(debug=True)
