# Flask config
DEBUG = True
SECRET_KEY = "SECRET_KEY"

# OAuth config
GITHUB_OAUTH_CLIENT_ID = "oauth_client_id"
GITHUB_OAUTH_CLIENT_SECRET = "oauth_client_secret"
GITHUB_OAUTH_CALLBACK_URL = "http://127.0.0.1:5000/callback"

# Session configuration
SESSION_TYPE = 'filesystem'  # Set session data to be stored to a local server-side file
SESSION_USE_SIGNER = True
SESSION_COOKIE_SECURE = True