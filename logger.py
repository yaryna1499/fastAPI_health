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
    def format(self, record):
        log_record = {
            'time': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'name': record.name,
            'filename': record.filename,
            'line': record.lineno,
            'trace_id': getattr(record, 'otelTraceID', None),
            'span_id': getattr(record, 'otelSpanID', None),
            'service_name': getattr(record, 'otelServiceName', None),
            'message': record.getMessage(),
        }
        return json.dumps(log_record)


# stream_handler.setFormatter(JSONFormatter())
