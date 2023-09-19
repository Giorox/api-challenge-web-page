from flask import Blueprint, render_template, redirect, request, session, url_for, current_app, abort
import requests as rq
import secrets

from funcs import User, Competition

user_blueprint = Blueprint('user', __name__)


# -----------------------------------------------------------------------------------------------
# ------------------------------------ LOGIN AND USER ROUTES ------------------------------------
# -----------------------------------------------------------------------------------------------
@user_blueprint.route("/login", methods=["GET"])
def githubLogin():
    '''
    Start Github OAuth2 flow to authenticate a user
    '''
    firstPhaseURL = "https://github.com/login/oauth/authorize"  # First phase URL for OAuth2 authentication

    # Generate a state token (URL-safe 16-byte long) for XSF protection and set it to our session
    session["state"] = secrets.token_urlsafe(16)

    # Build the payload to request login through Github's OAuth2 flow
    payload = {
        "client_id": current_app.config["GITHUB_OAUTH_CLIENT_ID"],
        "redirect_uri": current_app.config["GITHUB_OAUTH_CALLBACK_URL"],
        "scope": "read:user, user:email",
        "state": session["state"]
    }

    # Hand build the request URL for the initial authentication procedure
    url = firstPhaseURL + "?" + '&'.join([f"{param}={value}" for param, value in payload.items()])

    return redirect(url)


@user_blueprint.route("/callback", methods=["GET"])
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
        "client_id": current_app.config["GITHUB_OAUTH_CLIENT_ID"],
        "client_secret": current_app.config["GITHUB_OAUTH_CLIENT_SECRET"],
        "code": code,
        "redirect_uri": current_app.config["GITHUB_OAUTH_CALLBACK_URL"]
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
    userObject = User(tokenResponse["access_token"])

    # Insert the user in our database, returns graciously if it already exists
    userObject.insertUser()

    # Update all non-github fields
    userObject.getUserDatabaseInfo()

    # Save the user object as a dict to our session
    session["user"] = userObject.toDict()

    # return session["user"]
    return redirect(url_for("home"))


@user_blueprint.route("/profile/<string:login>")
def profile(login):
    if User.isCurrentLoggedIn(login, session):
        profileData = session["user"]["user_details"]
    else:
        profileData = User.getUserInfoByLogin(login)  # Call function to pull user profile (not the logged in one)
        # If the user does not exist, return a 404
        if profileData is None:
            abort(404)

    return render_template("profile.html", profile=profileData)


@user_blueprint.route("/score/<string:login>")
def score(login):
    return Competition.getUserScoreByName(login)


@user_blueprint.route("/scoreboard")
def scoreboard():
    ...


@user_blueprint.route("/logout")
def logout():
    # Explicitly pop user and state variables from current session
    session.pop("user")
    session.pop("state")

    # Clear the rest of the session
    session.clear()

    # Redirect to home
    return redirect(url_for("home"))
