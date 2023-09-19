import os

# Flask config
DEBUG = True
SECRET_KEY = "SECRET_KEY"

# OAuth config
GITHUB_OAUTH_CLIENT_ID = "cc1c20c4b4ff33cecfa3"
GITHUB_OAUTH_CLIENT_SECRET = "a844cf4aa757015605e50721f3011e595bafe980"
GITHUB_OAUTH_CALLBACK_URL = f"http://127.0.0.1:{os.environ.get('PORT')}/callback"

# Session configuration
SESSION_TYPE = 'filesystem'  # Set session data to be stored to a local server-side file
SESSION_USE_SIGNER = True
SESSION_COOKIE_SECURE = True

# Database config
DATABASE_PARAMETERS = {
    "host": os.environ.get("DB_HOST") or "database",
    "port": os.environ.get("DB_PORT") or "5432",
    "database": os.environ.get("DB_NAME") or "api-web-db",
    "user": os.environ.get("DB_USER") or "postgres",
    "password": os.environ.get("DB_PASSWORD") or "secret"
}
