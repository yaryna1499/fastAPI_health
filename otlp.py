from logger import logger
import logging
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import (
    OTLPLogExporter,
)
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from starlette.types import ASGIApp
from opentelemetry.instrumentation.logging import LoggingInstrumentor

def set_otlp(app: ASGIApp, app_name: str, otlp_endp: str):
    resource = Resource.create({"service.name": app_name,})
    # TRACING
    # set the tracer provider
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)
    tracer.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=otlp_endp)))
    # LOGGING
    # create the providers
    logger_provider = LoggerProvider(resource=resource)
    # set the providers
    set_logger_provider(logger_provider)
    exporter = OTLPLogExporter(endpoint=otlp_endp, timeout=5, insecure=True)
    # add the batch processors to the trace provider
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)
    # formatter = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] [trace_id=%(otelTraceID)s span_id=%(otelSpanID)s resource.service.name=%(otelServiceName)s] - %(message)s")
    # handler.setFormatter(formatter)
    logger.addHandler(handler)
    # LoggingInstrumentor().instrument(set_logging_format=True)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)