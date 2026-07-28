from flask import Flask

import os
from app.config import config
from flask_cors import CORS
from app.extensions import (
    db,
    migrate,
    bcrypt,
    jwt,
    mail,
)


def create_app():

    app = Flask(__name__)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://127.0.0.1:5501", "http://10.176.84.179:5501"]
            }
        },
        supports_credentials=True,
    )
    config_name = os.getenv("FLASK_ENV", "development")
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Import models
    from app import models

    # Register routes
    from app.routes.health import health_bp

    app.register_blueprint(health_bp)

    # Register auth routes
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)

    # Register survey routes
    from app.routes.survey import survey_bp

    app.register_blueprint(survey_bp)

    return app


# Survey,
# Question,
# Option,
# Response,
# Answer,
