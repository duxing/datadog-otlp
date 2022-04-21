from web import app
import redis
import os

# OpenTelemetry implementation
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter
)

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
RedisInstrumentor().instrument()

trace.set_tracer_provider(TracerProvider())

app.logger.info(f'creating opentelemetry tracer. name={__name__}')

tracer = trace.get_tracer(__name__)

# Datadog listens on port 4317(grpc) for OTLP ingestion
# 'datadog' is the hostname in local docker network
otlp_exporter = OTLPSpanExporter(endpoint="http://datadog:4317", insecure=True)

trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# for debugging via console
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


# initialize Redis
redis_host = os.getenv('REDIS_HOST')
redis_port = os.getenv('REDIS_PORT')

app.logger.info(f'connecting to Redis. host={redis_host} port={redis_port}')

redis_client = redis.StrictRedis(host=redis_host, port=redis_port)


@app.route('/')
def index():
    return 'ok'


@app.route('/ot')
def ot():
    with tracer.start_as_current_span('ot'):
        app.logger.info('Hello world from OpenTelemetry Python!')
    return 'ok'


@app.route('/redis/<key>')
def redis_get(key):
    return str(redis_client.get(key))

