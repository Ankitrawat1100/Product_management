from flask import jsonify
from werkzeug.exceptions import HTTPException


class AppError(HTTPException):
    code = 400
    description = "Application Error"


class NotFoundError(AppError):
    code = 404


class ConflictError(AppError):
    code = 409


class BadRequestError(AppError):
    code = 400


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(err: AppError):
        resp = {"error": err.__class__.__name__, "message": err.description}
        return jsonify(resp), err.code

    @app.errorhandler(HTTPException)
    def handle_http_error(err: HTTPException):
        resp = {"error": "HTTPException", "message": err.description}
        return jsonify(resp), err.code

    @app.errorhandler(Exception)
    def handle_unexpected(err: Exception):  # noqa: BLE001
        app.logger.exception("unexpected.error", extra={"error": str(err)})
        return jsonify({"error": "InternalServerError", "message": "Something went wrong"}), 500
