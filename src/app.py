import os

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, json
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from werkzeug.exceptions import HTTPException

from src.models import db

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
ma = Marshmallow()

spec = APISpec(
    title="Dio Blog",
    version="1.0.0",
    openapi_version="3.1.0",
    info=dict(description="Dio Blog Api"),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)


def create_app(environment=os.environ["ENVIRONMENT"]):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(f"src.config.{environment.title()}Config")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    ma.init_app(app)

    # register blueprint
    from src.controllers import auth, role, user

    app.register_blueprint(user.app)
    app.register_blueprint(role.app)
    app.register_blueprint(auth.app)

    @app.route("/docs")
    def docs():
        return spec.path(view=user.get_user).path(view=user.delete_user).to_dict()

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()

        response.data = json.dumps({"code": e.code, "name": e.name, "description": e.description})
        response.content_type = "application/json"
        return response

    return app
