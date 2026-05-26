import os
from flask import Flask
from config import config
from extensions import db


def create_app(config_name=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name or os.getenv("APP_ENV", "development")])

    db.init_app(app)

    from routes.destinations import bp
    app.register_blueprint(bp)

    from errors import register_error_handlers
    register_error_handlers(app)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    create_app().run()
