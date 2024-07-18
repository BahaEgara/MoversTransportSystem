import flask
import flask_login
import flask_moment
import flask_mailman
import flask_bootstrap
import flask_sqlalchemy

from config import config

# Set endpoint for the login page
login_manager = flask_login.LoginManager()
login_manager.blueprint_login_views = {
    "administrators": "authentication.administrator_login",
    "loaders": "authentication.loader_login",
    "drivers": "authentication.driver_login",
    "retailers": "authentication.retailer_login",
    "farmers": "authentication.farmer_login",
    "authentication": "authentication.farmer_login",
    "main": "authentication.client_login",
}


@login_manager.user_loader
def load_user(user_id):
    from .models import Loader
    from .models import Driver
    from .models import Farmer
    from .models import Retailer
    from .models import Administrator

    user_type = flask.session.get("user_type")
    if user_type == "loader":
        user = Loader.query.get(int(user_id))

    elif user_type == "driver":
        user = Driver.query.get(int(user_id))

    elif user_type == "farmer":
        user = Farmer.query.get(int(user_id))

    elif user_type == "administrator":
        user = Administrator.query.get(int(user_id))

    elif user_type == "retailer":
        user = Retailer.query.get(int(user_id))

    else:
        user = None

    return user


db = flask_sqlalchemy.SQLAlchemy()
mail = flask_mailman.Mail()
bootstrap = flask_bootstrap.Bootstrap()
moment = flask_moment.Moment()


def create_app(config_name="default"):
    """
    Initialize and configure the Flask application.

    :param config_name: str - The name of the configuration class defined in
        config.py.

    :return app: Flask - The configured Flask application instance.
    """
    app = flask.Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    # Enable SSL redirection if configured
    if app.config["SSL_REDIRECT"]:
        from flask_sslify import SSLify

        SSLify(app)

    # Register blueprints for different parts of the application
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .authentication import authentication as authentication_blueprint

    app.register_blueprint(authentication_blueprint, url_prefix="/auth")

    from .drivers import drivers as drivers_blueprint

    app.register_blueprint(drivers_blueprint, url_prefix="/driver")

    from .loaders import loaders as loaders_blueprint

    app.register_blueprint(loaders_blueprint, url_prefix="/loader")

    from .retailers import retailers as retailers_blueprint

    app.register_blueprint(retailers_blueprint, url_prefix="/retailer")

    from .farmers import farmers as farmers_blueprint

    app.register_blueprint(farmers_blueprint, url_prefix="/farmer")

    from .administrators import administrators as administrators_blueprint

    app.register_blueprint(
        administrators_blueprint, url_prefix="/administrator"
    )

    return app
