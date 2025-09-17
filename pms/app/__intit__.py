from flask import Flask, jsonify
from .config import Config
from .logger import configure_logging
from .exceptions import register_error_handlers
from .models import db
from .routes import bp as api_bp


def create_app(config_object: type = Config) -> Flask:
    configure_logging()
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    register_error_handlers(app)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return jsonify(status="ok"), 200

    with app.app_context():
        db.create_all()

    return app