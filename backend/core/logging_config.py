import logging
import json
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


class JSONFormatter(logging.Formatter):

    def format(self, record):

        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # ---------- Structured Fields ----------
        structured_fields = [
            "request_id",
            "query",
            "latency",
            "visualization",
            "tokens_input",
            "tokens_output",
            "hallucination_detected",
        ]

        for field in structured_fields:
            if hasattr(record, field):
                key = (
                    "latency_seconds"
                    if field == "latency"
                    else field
                )
                log_record[key] = getattr(record, field)

        # ---------- Exception ----------
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_logging():

    import sys

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    log_dir = os.path.join(BASE_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, "app.log")

    print("LOG FILE PATH:", log_file)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    formatter = JSONFormatter()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
    )

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)