import contextvars
import json
import logging
import time
from logging.handlers import RotatingFileHandler


class JSONLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "correlation_id": correlation_id_ctx.get(),
            "timestamp": int(time.time() * 1000),
            "level": record.levelname,
            "pathname": record.pathname,
            "lineno": record.lineno,
            "process_id": record.process,
            "message": record.getMessage(),
        }

        if hasattr(record, "extra_data") and isinstance(record.extra_data, dict):
            log_record.update(record.extra_data)
        
        return json.dumps(log_record)


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id_ctx.get("-")
        return True


def get_logger():
    handler = RotatingFileHandler(
        filename="logs/app.log",
        maxBytes=5*1024*1024,
        backupCount=5,
        encoding="utf-8",
    )
    handler.setFormatter(JSONLogFormatter())
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.addFilter(CorrelationIdFilter("CorrelationIdFilter"))
    return logger


correlation_id_ctx = contextvars.ContextVar("correlation_id", default="-")
logger = get_logger()