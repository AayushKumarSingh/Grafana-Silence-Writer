import logging
import json
import os.path
from datetime import datetime, timezone

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Create log file if doesn't exists
os.makedirs(LOG_DIR, exist_ok=True)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "module": record.module,
            "function_name": record.funcName,
            "message": record.getMessage()
        }

        # Extra Log information to be passed in each log type
        if hasattr(record, "instance"):
            log_record["instance"] = record.instance

        return json.dumps(log_record)


class AppLogger:
    def __init__(self, LOG_FILE):
        self.logger = logging.getLogger("fastapi_app")
        self.logger.setLevel(logging.INFO)

        # Put logs in given file location
        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(JsonFormatter())

        # Display captured logs in console
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(JsonFormatter())

        if not self.logger.handlers:
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def info(self, message, user="System"):
        self.logger.info(message, extra={"instance": user}, stacklevel=2)

    def error(self, message, user="System"):
        self.logger.error(message, extra={"instance": user}, stacklevel=2)

    def exception(self, message, user="System"):
        self.logger.exception(message, extra={"instance": user}, stacklevel=2)


logger = AppLogger(LOG_FILE)
