from flask import Blueprint, render_template

error_blueprint = Blueprint('error', __name__)


# -----------------------------------------------------------------------------------------------
# ----------------------------------------- ERROR PAGES -----------------------------------------
# -----------------------------------------------------------------------------------------------
@error_blueprint.app_errorhandler(404)
def notFound(error):
    return render_template('errors/404.html'), 404


@error_blueprint.app_errorhandler(500)
def internalServer(error):
    return render_template('errors/500.html'), 500
