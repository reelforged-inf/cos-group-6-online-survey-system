from flask import Flask

from app.config import DevelopmentConfig

from app.extensions import (
    db,
    migrate,
    bcrypt,
    jwt,
    mail,
)

def create_app():

    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)

    print(app.config["SQLALCHEMY_DATABASE_URI"])

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    # Import models
    from app.models import (
        User
    )



    # Register routes
    from app.routes.health import health_bp

    app.register_blueprint(health_bp)

    # Register auth routes
    from app.routes.auth import auth_bp

    app.register_blueprint(auth_bp)


    return app

 # Survey,
        # Question,
        # Option,
        # Response,
        # Answer,