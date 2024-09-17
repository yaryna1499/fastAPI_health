import logging
from pythonjsonlogger.jsonlogger import JsonFormatter


class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1

logger = logging.getLogger("fast-api-custom-logger")
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(JsonFormatter("%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s"))
logger.addHandler(stream_handler)
logger.addFilter(EndpointFilter())
