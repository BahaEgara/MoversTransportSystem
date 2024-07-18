from flask import Blueprint
from flask import session
from flask import current_app
from flask_cors import CORS


administrators = Blueprint("administrators", __name__)
from . import views, errors

# Enable CORS for the 'administrators' blueprint
CORS(administrators, supports_credentials=True)


@administrators.app_context_processor
def global_variables():
    """
    Provide global variables for templates within the 'administrators' blueprint.

    :return: A dictionary containing global variables to inject into templates.
    :rtype: dict

    :params: None
    """
    return dict(
        user_type=session.get("user_type"),
        app_name=current_app.config["ORGANIZATION_NAME"],
    )
