import logging

class ContextFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "request_id"):
            record.request_id = "-"
        return True


logger = logging.getLogger("ai_app")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(levelname)s %(message)s request_id=%(request_id)s"
)

handler.setFormatter(formatter)
handler.addFilter(ContextFilter())

logger.handlers.clear()
logger.addHandler(handler)
logger.propagate = False
