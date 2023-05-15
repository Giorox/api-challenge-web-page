# Built-in and Third-party modules
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
import requests as rq
import secrets
# Self authored modules
from funcs import User

app = Flask(__name__)


# -----------------------------------------------------------------------------------------------
# ----------------------------------- MAIN APPLICATION ROUTES -----------------------------------
# -----------------------------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------------------------------------------------------------------------
# ------------------------------------ LOGIN AND USER ROUTES ------------------------------------
# -----------------------------------------------------------------------------------------------
@app.route("/login", methods=["GET"])
def githubLogin():
    '''
    Start Github OAuth2 flow to authenticate a user
    '''
    firstPhaseURL = "https://github.com/login/oauth/authorize"  # First phase URL for OAuth2 authentication

    # Generate a state token (URL-safe 16-byte long) for XSF protection and set it to our session
    session["state"] = secrets.token_urlsafe(16)

    # Build the payload to request login through Github's OAuth2 flow
    payload = {
        "client_id": app.config["GITHUB_OAUTH_CLIENT_ID"],
        "redirect_uri": app.config["GITHUB_OAUTH_CALLBACK_URL"],
        "scope": "user,repo:status",
        "state": session["state"]
    }

    # Hand build the request URL for the initial authentication procedure
    url = firstPhaseURL + "?" + '&'.join([f"{param}={value}" for param, value in payload.items()])

    return redirect(url)


@app.route("/callback", methods=["GET"])
def getAuthCallback():
    '''
    Receive Github OAuth2 session information (phase 2) after successful user login
    '''
    # Get state and code from request parameters
    state = request.args.get('state')
    code = request.args.get('code')

    # Check if the session's state matches the state given in the callback. If not, redirect to error and abort
    if session["state"] != state:
        session.pop("state", None)
        return redirect(url_for("home"), code=302)  # Error or home, with HTTP 302 redirect code (maybe error?)

    # Build JSON payload for token request, set destination url and configure all request headers
    secondPhaseURL = "https://github.com/login/oauth/access_token"
    payload = {
        "client_id": app.config["GITHUB_OAUTH_CLIENT_ID"],
        "client_secret": app.config["GITHUB_OAUTH_CLIENT_SECRET"],
        "code": code,
        "redirect_uri": app.config["GITHUB_OAUTH_CALLBACK_URL"]
    }
    headers = {"Accept": "application/json"}

    # Call POST with built parameters and catch response
    try:
        tokenRequest = rq.post(secondPhaseURL, data=payload, headers=headers)
        tokenRequest.raise_for_status()
    except rq.exceptions.HTTPError as err:
        print(f"HTTP ERROR: {err}")

    # Once we've established there are no HTTP errors, get the JSON response and check if there are any problems
    tokenResponse = tokenRequest.json()

    if 'error' in tokenResponse.keys():
        raise rq.exceptions.HTTPError(tokenResponse)

    # Create a user object that will store all user data, initialize it with OAuth Access Token
    session["user"] = User(tokenResponse["access_token"]).toDict()

    # return session["user"]
    return redirect(url_for("home"))


@app.route("/profile/<string:username>")
def profile(username):
    if username == session["user"]["user_details"]["login"]:
        profileData = session["user"]
    else:
        ...  # Call function to pull user profile

    return render_template("profile.html", profile=profileData)


@app.route("/score/<string:username>")
def score(username):
    ...


@app.route("/scoreboard")
def scoreboard():
    ...


@app.route("/logout")
def logout():
    # Explicitly pop user and state variables from current session
    session.pop("user")
    session.pop("state")

    # Clear the rest of the session
    session.clear()

    # Redirect to home
    return redirect(url_for("home"))


# -----------------------------------------------------------------------------------------------
# ----------------------------------------- ERROR PAGES -----------------------------------------
# -----------------------------------------------------------------------------------------------
@app.errorhandler(404)
def notFound(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internalServer(error):
    return render_template('errors/500.html'), 500


if __name__ == "__main__":
    # Load config
    app.config.from_object("config.config")

    # Configure Flask-Session
    Session(app)

    # Run app with desired config parameters
    app.run(debug=app.config["DEBUG"])
