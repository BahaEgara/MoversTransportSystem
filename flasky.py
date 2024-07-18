"""
Module: flasky.py
Description:
"""
import os

import flask
from flask_migrate import Migrate
from flask_migrate import upgrade


from app import db
from app import create_app


app = create_app(os.getenv("FLASK_CONFIG") or "default")
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    """
    Make application objects available in the Python Flask Interactive Shell
    """
    return dict(db=db)


@app.context_processor
def inject_global_variables():
    """Make application objects available to templates"""
    user_type = flask.session.get("user_type", "farmer")

    return dict(user_type=user_type)


# =============================================================================
# Most errorhandlers will simply work as expected; however, there is a caveat
# concerning handlers for 404 and 405 exceptions. These errorhandlers are
# only invoked from an appropriate raise statement or a call to abort in
# another of the blueprint’s view functions; they are not invoked by, e.g.,
# an invalid URL access. This is because the blueprint does not “own” a
# certain URL space, so the application instance has no way of knowing which
# blueprint error handler it should run if given an invalid URL.
# =============================================================================
@app.errorhandler(404)
@app.errorhandler(405)
def _handle_blueprint_404_errors(ex):
    # Check if the request accepts json responses
    if (
        flask.request.accept_mimetypes.accept_json
        and not flask.request.accept_mimetypes.accept_html
    ):
        return flask.jsonify({"error": f"{ex.description}"}), ex.code

    # By default, use error pages on the base templates folder
    folder = ""

    # A tuple of blueprints of interest
    blueprints = ("farmer", "retailer", "administrator", "loader", "driver")

    # Retrieve logged in user type
    user_type = flask.session.get("user_type")

    # Determine folder based on blueprint path and user type
    for blueprint in blueprints:
        if (
            flask.request.path.startswith(f"/{blueprint}/")
            and user_type == blueprint
        ):
            folder = f"{blueprint}s/"
            break

    return flask.render_template(f"{folder}/{ex.code}.html"), ex.code


if __name__ == "__main__":
    app.run()
