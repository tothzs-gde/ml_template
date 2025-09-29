import contextvars
import logging
from logging.handlers import RotatingFileHandler


class RequestIdFilter(logging.Filter):
    def __init__(self, ctx, name = ""):
        super().__init__(name)
        self._ctx = ctx

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = self._ctx.get("-")
        return True


def _instantiate_logger():
    logger = logging.getLogger("app")
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - [request_id=%(request_id)s] - %(message)s"
    )
    handler = RotatingFileHandler(
        filename="app",
        maxBytes=5*1024*1024,
        backupCount=5,
        encoding="utf-8",
    )
    handler.setFormatter(formatter)
    handler.addFilter(
         RequestIdFilter(request_id_ctx, name="request_id_filter")
    )

    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger


request_id_ctx = contextvars.ContextVar("request_id", default="-")
logger = _instantiate_logger()