"""OpenTelemetry instrumentation and setup."""

import logging
import socket
from typing import Optional
from urllib.parse import urlparse
from fastapi import FastAPI

from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from app.core.config import settings
from app.core.database import async_engine

logger = logging.getLogger(__name__)


def _is_otlp_endpoint_reachable(endpoint: str) -> bool:
    """Return True if OTLP endpoint host:port is reachable."""
    if not endpoint:
        return False

    parsed = urlparse(endpoint)
    host = parsed.hostname
    port = parsed.port

    if not host:
        return False

    if port is None:
        port = 443 if parsed.scheme == "https" else 4317

    try:
        with socket.create_connection((host, port), timeout=0.5):
            return True
    except OSError:
        return False


def setup_otel(app: Optional[FastAPI] = None) -> None:
    """Initialize OpenTelemetry instrumentation.

    If `app` is provided, FastAPI instrumentation will be applied. When called
    without an app (e.g., during module import) FastAPI instrumentation is
    skipped to avoid instrumenting a None object.
    """
    if not settings.otel_enabled:
        logger.info("OpenTelemetry is disabled")
        return

    if (
        settings.otel_exporter_type == "otlp"
        and not _is_otlp_endpoint_reachable(settings.otel_exporter_otlp_endpoint)
    ):
        logger.warning(
            "OTLP endpoint %s is unreachable; skipping OpenTelemetry exporter setup",
            settings.otel_exporter_otlp_endpoint,
        )
        return

    try:
        # Setup Trace Provider
        trace_provider = TracerProvider()

        if settings.otel_exporter_type == "otlp":
            otlp_exporter = OTLPSpanExporter(
                endpoint=settings.otel_exporter_otlp_endpoint,
            )
            trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
        elif settings.jaeger_enabled:
            from opentelemetry.exporter.jaeger.thrift import JaegerExporter  # noqa: PLC0415
            jaeger_exporter = JaegerExporter(
                agent_host_name=settings.jaeger_agent_host,
                agent_port=settings.jaeger_agent_port,
            )
            trace_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

        trace.set_tracer_provider(trace_provider)

        # Setup Metrics Provider
        metric_reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(endpoint=settings.otel_exporter_otlp_endpoint)
        )
        metrics_provider = MeterProvider(metric_readers=[metric_reader])
        metrics.set_meter_provider(metrics_provider)

        # Instrument FastAPI only when app instance is provided
        if app is not None:
            FastAPIInstrumentor.instrument_app(app=app)
        else:
            logger.debug("FastAPI app not provided; skipping FastAPI instrumentation")

        # Instrument SQLAlchemy (use sync engine if async engine exposes it)
        engine_to_instrument = getattr(async_engine, "sync_engine", async_engine)
        try:
            SQLAlchemyInstrumentor().instrument(engine=engine_to_instrument)
        except Exception:
            logger.debug("SQLAlchemy instrumentation failed; continuing without DB instrumentation")

        logger.info(
            f"OpenTelemetry initialized with {settings.otel_exporter_type} exporter"
        )
    except Exception as e:
        logger.error(f"Failed to setup OpenTelemetry: {e}")
        # Continue without OTel rather than failing the app startup


def get_tracer(name: str) -> trace.Tracer:
    """Get a tracer instance."""
    return trace.get_tracer(name)


def get_meter(name: str) -> metrics.Meter:
    """Get a meter instance."""
    return metrics.get_meter(name)
