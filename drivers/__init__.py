from flask import Blueprint
from flask import session
from flask import current_app
from flask_cors import CORS


drivers = Blueprint("drivers", __name__)
from . import views, errors

# Enable CORS for the 'drivers' blueprint
CORS(drivers, supports_credentials=True)


@drivers.app_context_processor
def global_variables():
    """
    Provide global variables for templates within the 'drivers' blueprint.

    :return: A dictionary containing global variables to inject into templates.
    :rtype: dict

    :params: None
    """
    return dict(
        user_type=session.get("user_type"),
        app_name=current_app.config["ORGANIZATION_NAME"],
    )
