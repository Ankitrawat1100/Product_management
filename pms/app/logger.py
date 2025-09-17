import json
import logging
import os
import sys
from flask import has_request_context, request


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if hasattr(record, "extra"):
            log_record.update(record.extra)
        # request context fields
        if has_request_context():
            log_record["path"] = request.path
            log_record["method"] = request.method
        if record.exc_info:
            log_record["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


def configure_logging():
    root = logging.getLogger()
    if root.handlers:
        return
    handler = logging.StreamHandler(sys.stdout)

    json_logs = os.getenv("JSON_LOGS", "1") == "1"
    level = os.getenv("LOG_LEVEL", "INFO").upper()

    if json_logs:
        handler.setFormatter(JsonFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))

    root.setLevel(level)
    root.addHandler(handler)
