import logging as _logging
import sys


logger = _logging.getLogger(__name__)
logger.setLevel(_logging.DEBUG)
_stream_handler = _logging.StreamHandler(sys.stdout)
_log_formatter = _logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
_stream_handler.setFormatter(_log_formatter)
logger.addHandler(_stream_handler)
