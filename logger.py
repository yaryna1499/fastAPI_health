import logging
import sys
import logging.handlers

class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1

logger = logging.getLogger("fast-api-custom-logger")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler(sys.stdout)
logger.addHandler(stream_handler)
logger.addFilter(EndpointFilter())

# json formatter

import json

class JSONFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__()

        self._ignore_keys = {"msg", "args"}

    def format(self, record: logging.LogRecord) -> str:
        message = record.__dict__.copy()
        message["message"] = record.getMessage()

        for key in self._ignore_keys:
            message.pop(key, None)

        if record.exc_info and record.exc_text is None:
            record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message["exc_info"] = record.exc_text

        if record.stack_info:
            message["stack_info"] = self.formatStack(record.stack_info)

        return json.dumps(message)


# stream_handler.setFormatter(JSONFormatter())
