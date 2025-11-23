CREATE TABLE logs (
    log_id UUID,
    timestamp DateTime64(3, 'UTC'),
    severity LowCardinality(String),
    source_type LowCardinality(String),
    service_name String,
    host String,
    host_ip IPv4,
    message String,
    raw_message String,
    trace_id String,
    span_id String,
    metadata String
)
ENGINE = MergeTree
ORDER BY timestamp;

SELECT count() FROM logs;

INSERT INTO logs (
    log_id,
    timestamp,
    severity,
    source_type,
    service_name,
    host,
    host_ip,
    message,
    raw_message,
    trace_id,
    span_id,
    metadata
) VALUES (
    generateUUIDv4(),
    '2025-11-23 18:45:12.500',
    'ERROR',
    'server',
    'nginx',
    'gcp-vm-3',
    '10.128.0.42',
    'Nginx failed to reach backend',
    'GET /api/v1/user 502 120ms upstream error',
    'trace-89123',
    'span-backend',
    '{"method":"GET","path":"/api/v1/user","status_code":502,"latency_ms":120,"upstream":"backend-service"}'
);

SELECT * FROM logs LIMIT 10;