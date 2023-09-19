# Built-in and Third-party modules
from flask import Flask, render_template
from flask_session import Session
import os
# Self authored modules
from config import config, config_local
from routes.error import error_blueprint
from routes.user import user_blueprint

app = Flask(__name__)


# -----------------------------------------------------------------------------------------------
# ----------------------------------- MAIN APPLICATION ROUTES -----------------------------------
# -----------------------------------------------------------------------------------------------
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    # Load config
    if bool(os.environ.get('LOCAL', True)):
        app.config.from_object(config_local)
    else:
        app.config.from_object(config)

    # Register routes
    app.register_blueprint(error_blueprint)  # Errors
    app.register_blueprint(user_blueprint)  # User routes

    # Configure Flask-Session
    Session(app)

    # Run app with desired config parameters
    port = int(os.environ.get('PORT', 8080))
    host = str(os.environ.get('HOST', '0.0.0.0'))
    app.run(host=host, port=port, debug=app.config["DEBUG"])
